#!/usr/bin/python

"""Parse CSV file containing tile numbers and update a XuV projectfile with this information.
"""

# TODO:
#  - use pyhton's csv module
#  - parse tile size (pixels and real units) from the .xuv file
#  - parse tile position information from CSV file
#  - generate new position information
#  - update corresponding lines in .xuv file

file = open('tiles-arrangement.csv')
for line in file:
	for num in line.rsplit(';'):
		if num.isdigit():
			print int(num)


# >>> import csv
# >>> spamReader = csv.reader(open('eggs.csv', 'rb'), delimiter=' ', quotechar='|')
# >>> for row in spamReader:
# ...     print ', '.join(row)
# Spam, Spam, Spam, Spam, Spam, Baked Beans
# Spam, Lovely Spam, Wonderful Spam
