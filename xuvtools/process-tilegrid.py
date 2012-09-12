#!/usr/bin/python

"""Parse CSV file containing tile numbers and update a XuV projectfile with this information.
"""

# TODO:
#  - parse tile size (pixels and real units) from the .xuv file
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

parsedata = csv.reader(open('tiles-arrangement.csv'), delimiter=';')
data = [] # the 2D-list holding our tile numbers

# parse elements of the row and discard all non-numerical ones:
for row in parsedata:
    row_num = [] # holds the converted numerical values
    for num in row:
        if num.isdigit():
            row_num.append(int(num))
        else:
            row_num.append(None)
    # the last entry holds the maxval of this line, we discard it:
    data.append(row_num[0:-1])

print data
