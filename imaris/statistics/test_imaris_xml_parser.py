#!/usr/bin/python

from imaris_xml_parser import ImarisXML

XML = ImarisXML('__testdata/spots_red_multi_ws-all.xml', debug=2)
XML.celldata('Position')
