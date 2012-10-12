#!/usr/bin/python

"""Parse a CSV file containing filament point coordinates extracted from
Imaris via the XT/Matlab interface.
"""

# TODO:

import sys
import csv
import argparse
from dist_tools import dist_matrix_euclidean, get_max_dist_pair

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

def plot_3d(data1, data2, color1, color2):
    # stuff required for matplotlib:
    import matplotlib.pyplot as plt
    from numpy import asarray
    from mpl_toolkits.mplot3d import Axes3D

    # we need to have the coordinates as 3 ndarrays (x,y,z):
    x1,y1,z1 = asarray(zip(*data1))
    x2,y2,z2 = asarray(zip(*data2))
    # print x,y,z

    fig = plt.figure()
    ax = fig.gca(projection='3d')
    ax.scatter(x1,y1,z1,zdir='z', c=color1)
    ax.scatter(x2,y2,z2,zdir='z', c=color2, linewidth=18)
    plt.show()

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
    max_dist_pair = get_max_dist_pair(distance_matrix)

    maxdist_points = []
    for point in max_dist_pair:
        maxdist_points.append(data[point])


    if args.showmatrix:
        print distance_matrix
        print max_dist_pair
        print maxdist_points

    if args.plot:
        plot_3d(data1=data, data2=maxdist_points, color1='w', color2='r')


if __name__ == "__main__":
    sys.exit(main())
