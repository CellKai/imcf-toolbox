#!/usr/bin/python

from volpy import Filament
from log import set_loglevel

basedir = 'TESTDATA/filaments/'
infile = basedir + 'testdata-filaments-small.csv'
outfile = basedir + 'result_filaments-small.txt'

set_loglevel(2)
flmnt = Filament(infile)

output = open(outfile, 'w')
output.write(str(flmnt.get_coords()))
print 'Parsed %i points from "%s"' % \
    (len(flmnt.get_coords()), infile)
print('Written results to "%s"' % outfile)
