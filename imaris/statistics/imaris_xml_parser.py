#!/usr/bin/python

# TODO:
#  - do sanity checking
#  - evaluate datatypes from XML cells

import xml.etree.ElementTree as etree

class ImXMLError(Exception): pass

class ImarisXML:

    '''Parse Excel XML files into a python datastructure.
'''

    debug = 0
    tree = None

    def __init__(self, xmlfile, ns='', debug=0):
        self.set_debug(debug)
        tree = self.parse_xml(xmlfile)
#    tree1 = parse_xml(file1)
#    myns = check_namesp(tree1, 'urn:schemas-microsoft-com:office:spreadsheet')
#
#    tree2 = parse_xml(file2)
#    myns = check_namesp(tree2, 'urn:schemas-microsoft-com:office:spreadsheet')
#
#    # we're looking for stuff in the "Position" worksheet:
#    ws1_pos = get_worksheet(tree1, myns, 'Position')
#    ws2_pos = get_worksheet(tree2, myns, 'Position')
#
#    cells1 = parse_celldata(ws1_pos[0], myns)
#    cells2 = parse_celldata(ws2_pos[0], myns)


    def set_debug(self, level):
        self.debug = level

    def parse_xml(self, infile):
        if self.debug:
            print "Processing file: " + infile
        tree = etree.parse(infile)
        # print "Done parsing the XML."
        # print
        return(tree)

    def check_namesp(xml_etree, expected_ns):
        real_ns = xml_etree.getroot().tag[1:].split("}")[0]
        if not real_ns == expected_ns:
            print "ERROR, this file doesn't have the expected XML namespace!"
            sys.exit(1)
        # print "Namespace parsed from XML document: '" + real_ns + "'"
        # print
        return(real_ns)

    def get_worksheet(xml_etree, ns, pattern):
        pattern = ".//{%s}Worksheet[@{%s}Name='%s']" % (ns, ns, pattern)
        worksheet = xml_etree.findall(pattern)
        return(worksheet)

    def parse_celldata(worksheet, ns):
        cells = []
        rows = worksheet.findall('.//{%s}Row' % ns)
        for row in rows:
            content = []
            # check if this is a header row:
            style_att = '{%s}StyleID' % ns
            if style_att in row.attrib:
                # currently we don't process the header rows, so skip to the next
                continue
            # print str(len(row))
            for cell in row:
                content.append(cell[0].text)
            # print content
            cells.append(content)
        # print cells
        # cells is now [ [r1c1, r1c2, r1c3, ...],
        #                [r2c1, r2c2, r2c3, ...],
        #                [r3c1, r3c2, r3c3, ...],
        #                ...                      ]
        # print "Parsed rows: " + str(len(cells))
        return(cells)

