#!/usr/bin/python

"""Parse a CSV file containing filament point coordinates extracted from
Imaris via the XT/Matlab interface.
"""

# TODO:
#  - create a class for filaments, containing the coordinates list,
#    the distance matrix, the masks of the individual filaments,
#    access to start and end points, etc.

import sys
from csvtools import parse_float_tuples;
import argparse
import matplotlib.pyplot as plt
from numpy import ma
from dist_tools import dist_matrix_euclidean, get_max_dist_pair, \
    sort_neighbors, build_filament_mask, path_greedy, tesselate, remove_first_last


def build_tuple_seq(sequence, cyclic=False):
    """Convert a sequence into a list of 2-tuples.

    Takes a sequence (list) and returns a list of 2-tuples where
    each tuple consists of the previous list entry and the current one,
    starting with the entry (last, 1st), then (1st, 2nd) and so on.

    The optional parameter "cyclic" states whether the sequnce should
    by cyclic or acyclic, meaning the last and the first element will
    be connected or not.
    """
    # print sequence
    tuples = []
    for i, elt in enumerate(sequence):
        if i == 0:
            if cyclic:
                # use the last element as the predecessor of the first:
                prev = sequence[len(sequence) - 1]
            else:
                prev = elt
                continue
        tuples.append((prev, elt))
        prev = elt
    return tuples



def plot3d_prep():
    # stuff required for matplotlib:
    from mpl_toolkits.mplot3d import Axes3D
    fig = plt.figure()
    return fig.gca(projection='3d')


def plot3d_show():
    plt.show()


def plot3d_scatter(plot, points, color, lw=1):
    from numpy import asarray
    # we need to have the coordinates as 3 ndarrays (x,y,z):
    x, y, z = asarray(zip(*points))
    plot.scatter(x, y, z, zdir='z', c=color, linewidth=lw)


def plot3d_line(plot, points, color, lw=1):
    from numpy import asarray
    # we need to have the coordinates as 3 ndarrays (x,y,z):
    x, y, z = asarray(zip(*points))
    plot.plot(x, y, z, zdir='z', c=color)


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
    try:
        args = argparser.parse_args()
    except IOError as e:
        argparser.error(str(e))

    data = parse_float_tuples(args.infile)
    distance_matrix = dist_matrix_euclidean(data)
    maxdist_pair = get_max_dist_pair(distance_matrix)

    maxdist_points = []
    for point in maxdist_pair:
        maxdist_points.append(data[point])

    print '---------------------------------------------------'
    print 'points with largest distance: ' + str(maxdist_pair)
    print '   corresponding coordinates: ' + str(maxdist_points)
    print '      corresponding distance: ' + str(distance_matrix[maxdist_pair])
    print '---------------------------------------------------'

    if args.showmatrix:
        print distance_matrix

    adjacent = sort_neighbors(distance_matrix)
    # print adjacent

    # create an empty mask with the number of points:
    mask = [0] * len(distance_matrix[0])

    (p1, mask) = path_greedy(distance_matrix, mask, maxdist_pair)
    print 'path1 %s: %s' % (maxdist_pair, p1)
    (p2, mask) = path_greedy(distance_matrix, mask, maxdist_pair)
    print 'path2 %s: %s' % (maxdist_pair, p2)

    fil1 = remove_first_last(p1)
    fil2 = remove_first_last(p2)
    edges = tesselate(fil2, fil1, distance_matrix)
    # print "edges: %s" % edges

    if args.plot:
        plot = plot3d_prep()
        plot3d_scatter(plot, data, 'w')
        plot3d_scatter(plot, maxdist_points, 'r', lw=18)
        plot3d_line(plot, maxdist_points, 'y')
        for p in build_tuple_seq(adjacent, cyclic=True):
            coords = [data[p[0]], data[p[1]]]
            plot3d_line(plot, coords, 'm')

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

        print "edges (blue):  %s" % edges
        for p in edges:
            coords = [data[p[0]], data[p[1]]]
            plot3d_line(plot, coords, 'b')

        plot3d_show()


if __name__ == "__main__":
    sys.exit(main())
