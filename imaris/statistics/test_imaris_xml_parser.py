#!/usr/bin/python

from imaris_xml_parser import ImarisXML

namesp = 'urn:schemas-microsoft-com:office:spreadsheet'

XML = ImarisXML('__testdata/spots_green_single_ws-all.xml',
                namesp, debug=1)
