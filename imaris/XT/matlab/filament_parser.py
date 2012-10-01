#!/usr/bin/python

"""Parse a CSV file containing filament point coordinates extracted from
Imaris via the XT/Matlab interface.
"""

# TODO:

import sys
import csv
import argparse
from dist_tools import dist_matrix_euclidean, get_max_dist_pair

# stuff required for matplotlib:
import matplotlib.pyplot as plt
from numpy import asarray
from mpl_toolkits.mplot3d import Axes3D

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

def plot_3d(data):
    x,y,z = asarray(zip(*data))
    # print x,y,z

    fig = plt.figure()
    ax = fig.gca(projection='3d')
    ax.scatter(x,y,z,zdir='z', c='k')
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

    if args.showmatrix:
        print distance_matrix
        print max_dist_pair

    if args.plot:
        plot_3d(data)


if __name__ == "__main__":
    sys.exit(main())
