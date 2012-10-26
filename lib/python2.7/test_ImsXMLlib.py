#!/usr/bin/python

from ImsXMLlib import ImarisXML

XML = ImarisXML('__testdata/spots_red_multi_ws-all.xml', debug=1)
XML.celldata('Position')
