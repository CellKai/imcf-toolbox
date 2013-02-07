#!/usr/bin/python

"""Parse a CSV file containing filament point coordinates extracted from
Imaris via the XT/Matlab interface.
"""

# TODO:
#  - move the 3d plotting stuff somewhere else, especially the imports!
#  - merge the "filaments" and "volpy" modules, then use Filament objects

import sys
import argparse
import matplotlib.pyplot as plt
from matplotlib import cm
# stuff required for matplotlib:
from mpl_toolkits.mplot3d import Axes3D
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
from numpy import ma, loadtxt, asarray
from volpy import *
import pprint
import logging


def plot3d_prep():
    fig = plt.figure()
    return (fig.gca(projection='3d'), Axes3D(fig))

def plot3d_show():
    plt.show()

def plot3d_scatter(plot, points, color, lw=1):
    # we need to have the coordinates as 3 ndarrays (x,y,z):
    x, y, z = asarray(zip(*points))
    plot.scatter(x, y, z, zdir='z', c=color, linewidth=lw)

def plot3d_line(plot, points, color, lw=1):
    # we need to have the coordinates as 3 ndarrays (x,y,z):
    x, y, z = asarray(zip(*points))
    plot.plot(x, y, z, zdir='z', c=color)

def plot3d_triangle(plot, points, lw=0.2):
    x, y, z = asarray(zip(*points))
    plot.plot_trisurf(x, y, z, cmap=cm.jet, linewidth=lw)


def main():
    argparser = argparse.ArgumentParser(description=__doc__)
    argparser.add_argument('-i', '--infile', required=True, type=file,
        help='CSV file containing filament coordinates')
    argparser.add_argument('--plot', dest='plot', action='store_const',
        const=True, default=False,
        help='plot parsed filament data')
    argparser.add_argument('--showmatrix', dest='showmatrix',
        action='store_const', const=True, default=False,
        help='show the distance matrix and the longest distance pair')
    argparser.add_argument('-v', '--verbose', dest='verbosity',
        action='count', default=0)
    try:
        args = argparser.parse_args()
    except IOError as e:
        argparser.error(str(e))

    # default loglevel is 30 while 20 and 10 show more details
    loglevel = (3 - args.verbosity) * 10

    log = logging.getLogger(__name__)
    # create console handler and add it to the logger
    ch = logging.StreamHandler(sys.stdout)
    log.addHandler(ch)
    log.setLevel(loglevel)

    volpy_verbosity(loglevel)

    pp = pprint.PrettyPrinter(indent=4)

    # loadtxt() expects float numbers and complains otherwise
    data = loadtxt(args.infile, delimiter=',')

    distance_matrix = dist_matrix_euclidean(data)
    maxdist_pair = get_max_dist_pair(distance_matrix)

    log.debug(pp.pformat(data))
    log.info(pp.pformat(distance_matrix))

    maxdist_points = []
    for point in maxdist_pair:
        maxdist_points.append(data[point])

    print '------------ largest distance results -------------'
    print 'idx numbers:\t' + pp.pformat(maxdist_pair)
    print 'coordinates:\t' + pp.pformat(maxdist_points)
    print 'distance:\t' + pp.pformat(distance_matrix[maxdist_pair])
    print '---------------------------------------------------'


    adjacent = sort_neighbors(distance_matrix)
    log.debug(adjacent)

    # create an empty mask with the number of points:
    mask = [0] * len(distance_matrix[0])

    (p1, mask) = path_greedy(distance_matrix, mask, maxdist_pair)
    log.debug('path1 %s: %s' % (maxdist_pair, p1))
    (p2, mask) = path_greedy(distance_matrix, mask, maxdist_pair)
    log.debug('path2 %s: %s' % (maxdist_pair, p2))

    (edges, triangles, vertices) = tesselate(p2, p1, distance_matrix)
    print "vertices: %s" % vertices

    polyarea = 0
    vtxlist = []
    for (vrtx1, vrtx2, vrtx3) in triangles:
        vtxlist.append([tuple(data[vrtx1]),
            tuple(data[vrtx2]), tuple(data[vrtx3])])
        polyarea += tri_area(data[vrtx1], data[vrtx2], data[vrtx3])
    print "overall area: %s" % polyarea
    print "vtxlist: %s" % vtxlist


    if args.plot:
        # define some colors to cycle through:
        colors = ['r', 'b', 'y', 'm', 'g']
        plot, ax = plot3d_prep()
        plot3d_scatter(plot, data, 'w')
        plot3d_scatter(plot, maxdist_points, 'r', lw=18)
        plot3d_line(plot, maxdist_points, 'y')
        for p in build_tuple_seq(adjacent, cyclic=True):
            coords = [data[p[0]], data[p[1]]]
            plot3d_line(plot, coords, 'm')

        for vtx in vtxlist:
            tri = Poly3DCollection([vtx])
            ax.add_collection3d(tri)

        fm1, fma1 = build_filament_mask(adjacent, maxdist_pair)
        # compressed() returns only the unmasked entries
        filpnts1 = ma.array(adjacent, mask=fma1).compressed()
        # for p in build_tuple_seq(filpnts1):
        #     coords = [data[p[0]], data[p[1]]]
        #     plot3d_line(plot, coords, 'g')

        maxdist_pair = (maxdist_pair[1], maxdist_pair[0])
        fm2, fma2 = build_filament_mask(adjacent, maxdist_pair)
        # compressed() returns only the unmasked entries
        filpnts2 = ma.array(adjacent, mask=fma2).compressed()
        # for p in build_tuple_seq(filpnts2):
        #     coords = [data[p[0]], data[p[1]]]
        #     plot3d_line(plot, coords, 'b')

        for i, p in enumerate(edges):
            coords = [data[p[0]], data[p[1]]]
            curcol = colors[i % 5]
            plot3d_line(plot, coords, curcol)


        plot3d_show()


if __name__ == "__main__":
    sys.exit(main())
