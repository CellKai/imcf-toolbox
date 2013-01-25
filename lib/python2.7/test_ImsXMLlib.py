#!/usr/bin/python

from ImsXMLlib import ImarisXML

basedir = 'TESTDATA/spots_distances/'
infile = basedir + 'spots_red_multi_ws-all.xml'

XML = ImarisXML(open(infile), debug=1)
XML.celldata('Position')
