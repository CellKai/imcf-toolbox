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


data = [] # the 2D-list holding our tile numbers

# parse elements of the row, non-float values will raise a ValueError
parsedata = csv.reader(args.infile, delimiter=',', quoting=csv.QUOTE_NONNUMERIC)

for row in parsedata:
    row_num = [] # holds the converted numerical values
    for val in row:
        row_num.append(val)
    data.append(row_num)
print data
print len(data)
