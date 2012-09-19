#!/usr/bin/python

"""Parse a CSV file containing tile positions and update a Xuv projectfile with
this information.
"""

# WARNING: this script assumes *ALL* stacks in the project file do
# have the same size (x-y-z)!

# TODO:
#  - check if number of tiles from CSV matches .xuv file

import csv
import sys
import argparse

argparser = argparse.ArgumentParser(description=__doc__)
argparser.add_argument('-p', '--overlap', type=float, default='0.15',
    help='tile overlap (default 0.15)')
argparser.add_argument('-t', '--tiles', required=True, type=file,
    help='CSV file containing tile positions')
argparser.add_argument('-i', '--infile', required=True, type=file,
    help='Xuv input project file')
argparser.add_argument('-o', '--outfile', type=argparse.FileType('w', 0),
    help='Xuv input project file', required=True)
try:
    args = argparser.parse_args()
except IOError as e:
    argparser.error(str(e))

# print args.__contains__
# print type(args)
# print args.infile
# print args.outfile

data = [] # the 2D-list holding our tile numbers
tilemax = 0

# parse elements of the row and discard all non-numerical ones:
parsedata = csv.reader(args.tiles, delimiter=';')
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


# parse xuv project file, get tile size etc.
size_um = []
size_px = []
xuvdata_orig = []

for line in args.infile:
    # remember original xuv file content
    xuvdata_orig.append(line)
    # strip trailing whitespaces and split key-value pairs
    line_elt = line.rstrip().rsplit('=')
    if line_elt[0] == 'scene_element_size_um':
        for size in line_elt[1].rsplit(','):
            size_um.append(float(size))
    if line_elt[0] == 'stack0001_size_pix':
        for size in line_elt[1].rsplit(','):
            size_px.append(int(size))
args.infile.close()

print size_um
print size_px


# generate new xuv file content
for line in xuvdata_orig:
    line_elt = line.rstrip().rsplit('=')
    # scan for lines holding tile coordinates
    if line_elt[0].endswith('abs_pos_um'):
        prefix = line_elt[0].split('_', 1)[0]
        tileno = int(prefix[4:8])
        ## now calculate the new tile position
        coord_y = tilepos[tileno - 1][0] * (1 - args.overlap)
        coord_x = tilepos[tileno - 1][1] * (1 - args.overlap)
        coord_y = coord_y * size_px[1] * size_um[1]
        coord_x = coord_x * size_px[2] * size_um[2]
        args.outfile.write(line_elt[0] + '=0,'
            + str(coord_y) + ',' + str(coord_x) + '\n')
    else:
        args.outfile.write(line)
args.outfile.close()
