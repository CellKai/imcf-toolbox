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
from matplotlib.colors import colorConverter
# http://matplotlib.org/api/colors_api.html

# stuff required for matplotlib:
from mpl_toolkits.mplot3d import Axes3D
from mpl_toolkits.mplot3d.art3d import Poly3DCollection

from numpy import ma, loadtxt, asarray, linalg
from volpy import *
import pprint
import logging


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

def plot3d_maxdist(ax, maxdist_points):
    plot3d_scatter(ax, maxdist_points, 'r', lw=18)
    for i in (0,1):
        ax.text(*maxdist_points[i], color='blue',
            s='   (%s | %s | %s)' % (maxdist_points[i][0],
            maxdist_points[i][1], maxdist_points[i][2]))
    # draw connection line between points:
    plot3d_line(ax, maxdist_points, 'y')
    # calculate length and add label:
    pos = maxdist_points[1] + ((maxdist_points[0]-maxdist_points[1])/2)
    dist = linalg.norm(maxdist_points[0]-maxdist_points[1])
    ax.text(*pos, color='blue', s='%s' % dist)

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
    log.warn("overall area: %s" % polyarea)
    log.debug("vtxlist: %s" % vtxlist)


    if args.plot:
        # define some colors to cycle through:
        colors = ['r', 'g', 'b', 'y', 'c', 'm']
        cc = lambda arg: colorConverter.to_rgba(arg, alpha=0.6)

        # prepare the figure
        fig = plt.figure()
        ax = Axes3D(fig)

        # determine min and max coordinates and set limits:
        cmin = data.min(axis=0)
        cmax = data.max(axis=0)
        ax.set_xlim3d(cmin[0], cmax[0])
        ax.set_ylim3d(cmin[1], cmax[1])
        ax.set_zlim3d(cmin[2], cmax[2])

        # draw axis lables
        ax.set_xlabel('X')
        ax.set_ylabel('Y')
        ax.set_zlabel('Z')

        # draw the raw filament points:
        # TODO: add commandline switch to enable this!
        # plot3d_scatter(ax, data, 'w')

        # draw the maxdist pair and a connecting line + labels:
        plot3d_maxdist(ax, maxdist_points)

        # draw connections along filament lists:
        for p in build_tuple_seq(adjacent, cyclic=True):
            coords = [data[p[0]], data[p[1]]]
            plot3d_line(ax, coords, 'm')

        # draw edges from tesselation:
        for i, p in enumerate(edges):
            coords = [data[p[0]], data[p[1]]]
            curcol = colors[i % 6]
            plot3d_line(ax, coords, curcol)

        # draw triangles from tesselation as filled polygons:
        for i, vtx in enumerate(vtxlist):
            curcol = colors[i % 6]
            tri = Poly3DCollection([vtx], facecolors=cc(curcol))
            tri.set_alpha(0.8)
            ax.add_collection3d(tri)

        plt.show()


if __name__ == "__main__":
    sys.exit(main())
