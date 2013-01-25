#!/usr/bin/python

from ImsXMLlib import ImarisXML

basedir = 'TESTDATA/spots_distances/'
infile = basedir + 'spots_red_multi_ws-all.xml'
outfile = basedir + 'result_ImsXMLlib_sp_red_mult_all.txt'

print('Parsing "%s"' % infile)
XML = ImarisXML(open(infile), debug=0)
res = XML.celldata('Position')

output = open(outfile, 'w')
output.write(str(res))
print('Written results to "%s"' % outfile)
