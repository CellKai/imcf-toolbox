#!/usr/bin/python

"""Parse a CSV file containing filament point coordinates extracted from
Imaris via the XT/Matlab interface.
"""

# TODO:
#  - build data structure from coordinates

import csv
import argparse
from dist_tools import dist, largest_dist_idx

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
    # FIXME: should be num_val instead of row_num
    row_num = [] # holds the converted numerical values
    for val in row:
        row_num.append(val)
    data.append(row_num)
# print data
print 'Parsed ' + str(len(data)) + ' points from CSV file.'


# calculate longest distance pair:
maxdist_pair = [0, 0, 0.0]
for idx, point in enumerate(data):
    dist_tuple = largest_dist_idx(point, data)
    # print dist_tuple
    if dist_tuple[1] > maxdist_pair[2]:
        maxdist_pair = [idx] + dist_tuple
        print 'updating maxdist_pair: ' + str(maxdist_pair)
    # print str(point) + ' ' + str(dist_tuple)
