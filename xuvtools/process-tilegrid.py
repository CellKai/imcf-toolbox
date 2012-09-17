#!/usr/bin/python

"""Parse a CSV file containing tile positions and update a Xuv projectfile with
this information.
"""

# WARNING: this script assumes *ALL* stacks in the project file do
# have the same size (x-y-z)!

# TODO:
#  - check if number of tiles from CSV matches .xuv file
#  - use commandline parameters for input, output and overlap

import csv

overlap = 0.15 # set overlap to 15 percent

data = [] # the 2D-list holding our tile numbers
tilemax = 0

# parse elements of the row and discard all non-numerical ones:
parsedata = csv.reader(open('tiles-arrangement.csv'), delimiter=';')
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

xuvfile = open('file.xuv')
for line in xuvfile:
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
xuvfile.close()

print size_um
print size_px


# generate new xuv file content
xuvfile = open('newfile.xuv', 'w')
for line in xuvdata_orig:
    line_elt = line.rstrip().rsplit('=')
    # scan for lines holding tile coordinates
    if line_elt[0].endswith('abs_pos_um'):
        prefix = line_elt[0].split('_', 1)[0]
        tileno = int(prefix[4:8])
        ## now calculate the new tile position
        coord_y = tilepos[tileno - 1][0] * (1 - overlap)
        coord_x = tilepos[tileno - 1][1] * (1 - overlap)
        coord_y = coord_y * size_px[1] * size_um[1]
        coord_x = coord_x * size_px[2] * size_um[2]
        xuvfile.write(line_elt[0] + '=0,'
            + str(coord_y) + ',' + str(coord_x) + '\n')
    else:
        xuvfile.write(line)
xuvfile.close()
