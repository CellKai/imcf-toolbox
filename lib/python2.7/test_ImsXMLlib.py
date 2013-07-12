#!/usr/bin/python

from ImsXMLlib import ImarisXML
from log import log

log.setLevel(20)

basedir = 'TESTDATA/spots_distances/'
infile = basedir + 'spots_red_multi_ws-all.xml'
outfile = basedir + 'result_ImsXMLlib_sp_red_mult_all.txt'

# test with filehandle:
XML = ImarisXML(open(infile))
# test with string:
XML = ImarisXML(infile)
res = XML.celldata('Position')

output = open(outfile, 'w')
output.write(str(res))
print('Written results to "%s"' % outfile)
