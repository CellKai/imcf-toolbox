#!/usr/bin/python

from filaments import Filament

basedir = 'TESTDATA/filaments/'
infile = basedir + 'testdata-filaments-small.csv'
outfile = basedir + 'result_filaments-small.txt'

flmnt = Filament(open(infile), debug=0)

output = open(outfile, 'w')
output.write(flmnt.get_coords())
print 'Parsed %i points from "%s"' % \
    (len(flmnt.get_coords()), infile)
print('Written results to "%s"' % outfile)
