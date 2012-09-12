#!/usr/bin/python

"""Parse CSV file containing tile numbers and update a XuV projectfile with this information.
"""

# WARNING: this script assumes *ALL* stacks in the project file do
# have the same size (x-y-z)!

# TODO:
#  - parse tile position information from CSV file
#  - check if number of tiles from CSV matches .xuv file
#  - generate new position information
#  - update corresponding lines in .xuv file

# file = open('tiles-arrangement.csv')
# for line in file:
# 	for num in line.rsplit(';'):
# 		if num.isdigit():
# 			print int(num)


import csv

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

print data



# parse xuv project file, get tile size etc.
elt_size_um = []
elt_size_px = []
xuvdata_orig = []

xuvfile = open('file.xuv')
for line in xuvfile:
    # remember original xuv file content
    xuvdata_orig.append(line)
    # strip trailing whitespaces and split key-value pairs
    line_elt = line.rstrip().rsplit('=')
    if line_elt[0] == 'scene_element_size_um':
        for size in line_elt[1].rsplit(','):
            elt_size_um.append(float(size))
    if line_elt[0] == 'stack0001_size_pix':
        for size in line_elt[1].rsplit(','):
            elt_size_px.append(int(size))
xuvfile.close()

print elt_size_um
print elt_size_px
