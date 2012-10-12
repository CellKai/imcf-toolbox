#!/usr/bin/python

"""Parse a CSV file containing filament point coordinates extracted from
Imaris via the XT/Matlab interface.
"""

# TODO:

import sys
import csv
import argparse
import matplotlib.pyplot as plt
from dist_tools import dist_matrix_euclidean, get_max_dist_pair, sort_neighbors

def build_tuple_seq(sequence):
    """Convert a sequence into a list of 2-tuples.

    Takes a sequence (list) and returns a list of 2-tuples where
    each tuple consists of the previous list entry and the current one,
    starting with the entry (last, 1st), then (1st, 2nd) and so on.
    """
    tuples = []
    for i, elt in enumerate(sequence):
        if i == 0:
            prev = sequence[len(sequence) - 1]
        tuples.append((prev, elt))
        prev = elt
    return tuples

def parse_float_tuples(fname):
    """Parses every line of a CSV file into a tuple.

    Parses a CSV file, makes sure all the parsed elements are float
    values and assembles a 2D list of them, each element of the list
    being a n-tuple holding the values of a single line from the CSV.

    Args:
        fname: A filename of a CSV file.

    Returns:
        A list of n-tuples, one tuple for each line in the CSV, for
        example:

        [[1.3, 2.7, 4.22], [22.5, 3.2, 5.5], [2.2, 8.3, 7.6]]

    Raises:
        ValueError: The parser found a non-float element in the CSV.
    """
    parsedata = csv.reader(fname, delimiter=',', quoting=csv.QUOTE_NONNUMERIC)
    data = []
    for row in parsedata:
        num_val = []
        for val in row:
            num_val.append(val)
        data.append(num_val)
    # print data
    print 'Parsed ' + str(len(data)) + ' points from CSV file.'
    return data

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
    x,y,z = asarray(zip(*points))

    plot.scatter(x,y,z,zdir='z', c=color, linewidth=lw)

def plot3d_line(plot, points, color, lw=1):
    from numpy import asarray
    # we need to have the coordinates as 3 ndarrays (x,y,z):
    x,y,z = asarray(zip(*points))
    plot.plot(x,y,z,zdir='z', c=color)


def main():
    argparser = argparse.ArgumentParser(description=__doc__)
    argparser.add_argument('-i', '--infile', required=True, type=file,
        help='CSV file containing filament coordinates')
    argparser.add_argument('--plot', dest='plot', action='store_const',
        const=True, default=False,
        help='plot parsed filament data')
    argparser.add_argument('--showmatrix', dest='showmatrix', action='store_const',
        const=True, default=False,
        help='show the calculated distance matrix and the longest distance pair')
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

    adjacent = sort_neighbors(distance_matrix, data)


    if args.showmatrix:
        print distance_matrix
        print '---------------------------------------------------'
        print 'points with largest distance: ' + str(maxdist_pair)
        print '   corresponding coordinates: ' + str(maxdist_points)
        print '      corresponding distance: ' + str(distance_matrix[maxdist_pair])
        print '---------------------------------------------------'
        print adjacent

    if args.plot:
        plot = plot3d_prep()
        plot3d_scatter(plot, data, 'w')
        plot3d_scatter(plot, maxdist_points, 'r', lw=18)
        # FIXME: clean up this mess!!!
        tuples = build_tuple_seq(adjacent)
        # print tuples
        for p in tuples:
            print p
            coords = [data[p[0]], data[p[1]]]
            # print coords
            plot3d_line(plot, coords, 'r')

        plot3d_show()


if __name__ == "__main__":
    sys.exit(main())
