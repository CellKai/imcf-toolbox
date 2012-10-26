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
    namesp = ''

    def __init__(self, xmlfile, ns='', debug=0):
        self.set_debug(debug)
        self.namesp = ns
        self.parse_xml(xmlfile)
        self.check_namesp()
# TODO:
#    myns = check_namesp(tree1, 'urn:schemas-microsoft-com:office:spreadsheet')
#
#    ws1_pos = get_worksheet(tree1, myns, 'Position')
#
#    cells1 = parse_celldata(ws1_pos[0], myns)


    def set_debug(self, level):
        self.debug = level

    def parse_xml(self, infile):
        if self.debug:
            print "Processing file: " + infile
        self.tree = etree.parse(infile)
        if self.debug > 1:
            print "Done parsing the XML."
            print self.tree

    def check_namesp(self):
        real_ns = self.tree.getroot().tag[1:].split("}")[0]
        if not real_ns == self.namesp:
            if self.debug:
                print "ERROR, couldn't find the expected XML namespace!"
                print "Namespace parsed from XML: '" + real_ns + "'"
            raise(ImXMLError)

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

