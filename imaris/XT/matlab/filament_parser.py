#!/usr/bin/python

"""Parse a CSV file containing filament point coordinates extracted from
Imaris via the XT/Matlab interface.
"""

# TODO:
#  - parse CSV
#  - build data structure from coordinates

import csv
import argparse

argparser = argparse.ArgumentParser(description=__doc__)
argparser.add_argument('-i', '--infile', required=True, type=file,
    help='CSV file containing filament coordinates')
try:
    args = argparser.parse_args()
except IOError as e:
    argparser.error(str(e))

# print args.__contains__
# print type(args)
# print args.infile
# print args.outfile


# FIXME: check code below for re-using it

data = [] # the 2D-list holding our tile numbers
tilemax = 0

# parse elements of the row and discard all non-numerical ones:
parsedata = csv.reader(args.infile, delimiter=',')
for row in parsedata:
    row_num = [] # holds the converted numerical values
    for num in row:
        if num.isdigit():
            tile = int(num)
            row_num.append(tile)
            tilemax = max(tilemax, tile)
        else:
            row_num.append(None)
    # the last entry holds the maxval of this line, we discard it:
    data.append(row_num[0:-1])

# print data
# print tilemax

# construct a list of tuples with tile positions indexed by tile number
tilepos = [()] * tilemax
# print tilepos
for coord_y, line in enumerate(data):
    for coord_x, tile in enumerate(line):
        if not tile is None:
            tilepos[tile - 1] = (coord_y, coord_x)
print tilepos

