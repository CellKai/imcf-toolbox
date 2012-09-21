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

# parse elements of the row, non-float values will raise a ValueError
parsedata = csv.reader(args.infile, delimiter=',', quoting=csv.QUOTE_NONNUMERIC)

data = [] # the 2D-list holding our points
for row in parsedata:
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
