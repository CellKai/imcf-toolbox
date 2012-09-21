#!/usr/bin/python

"""Parse a CSV file containing filament point coordinates extracted from
Imaris via the XT/Matlab interface.
"""

# TODO:

import csv
import argparse
from dist_tools import dist_matrix_euclidean
from numpy.matlib import where

argparser = argparse.ArgumentParser(description=__doc__)
argparser.add_argument('-i', '--infile', required=True, type=file,
    help='CSV file containing filament coordinates')
try:
    args = argparser.parse_args()
except IOError as e:
    argparser.error(str(e))

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


data = parse_float_tuples(args.infile)

# Calculate the full distance matrix for all points using Euklid and
# determine the pair having the largest distance.
maxdist = 0
distance_matrix = dist_matrix_euclidean(data)
print distance_matrix
for row_num, row in enumerate(distance_matrix):
    row_max = max(row)
    if row_max > maxdist:
        maxdist = row_max
        print [row_num] + [where(row == row_max)[0][0]] + [maxdist]

