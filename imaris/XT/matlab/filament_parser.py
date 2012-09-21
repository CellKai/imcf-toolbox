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

# Now parse the file using the csv mechanisms to make sure we retrieve
# float values (non-floats will raise a ValueError), then assemble a
# 2D list of point-coordinates (tuples).
parsedata = csv.reader(args.infile, delimiter=',', quoting=csv.QUOTE_NONNUMERIC)
data = []
for row in parsedata:
    num_val = []
    for val in row:
        num_val.append(val)
    data.append(num_val)
# print data
print 'Parsed ' + str(len(data)) + ' points from CSV file.'

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

