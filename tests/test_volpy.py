#!/usr/bin/python

'''Test script for the "volpy" module.'''

from volpy import dist_matrix
from numpy import loadtxt, array_str, set_printoptions

basedir = 'TESTDATA/filaments/'
infile = basedir + 'testdata-filaments.csv'
outfile = basedir + 'result_volpy_fil_detailed.txt'

data = loadtxt(open(infile, 'r'), delimiter=',')
dist_mat = dist_matrix(data)

set_printoptions(threshold=999999)
outstr = array_str(dist_mat, max_line_width=999999)
output = open(outfile, 'w')
output.write(outstr)

print 'Parsed %i points from "%s"' % \
    (len(data), infile)
print('Written distance matrix to "%s"' % outfile)
