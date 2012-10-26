#!/usr/bin/python

# TODO:
#  - do sanity checking
#  - evaluate datatypes from XML cells

import xml.etree.ElementTree as etree

class ImXMLError(Exception): pass

class ImarisXML:

    '''Parse Excel XML files into a python datastructure.

       Structure returned by celldata() is a list of lists:
           [ [r1c1, r1c2, r1c3, ...],
             [r2c1, r2c2, r2c3, ...],
             [r3c1, r3c2, r3c3, ...],
             ...                      ]
'''

    debug = 0
    tree = None
    cells = {}
    # by default, we expect the namespace of Excel XML:
    namespace = 'urn:schemas-microsoft-com:office:spreadsheet'

    def __init__(self, xmlfile, ns='', debug=0):
        self.debug = debug
        self.parse_xml(xmlfile)
        if ns: self.namespace = ns
        self.check_namespace()


    def parse_xml(self, infile):
        """Aux function to call the etree parser.

        Just an auxiliary function for debugging statements.
        """
        if self.debug:
            print "Processing file: " + infile
        self.tree = etree.parse(infile)
        if self.debug > 1: print "Done parsing XML: " + str(self.tree)

    def check_namespace(self):
        """Check if an XML tree has a certain namespace.

        Takes an XML etree object and a string denoting the expected
        namespace, checks if the namespace of the XML tree matches.
        Returns the namespace if yes, exits otherwise.
        """
        real_ns = self.tree.getroot().tag[1:].split("}")[0]
        if not real_ns == self.namespace:
            if self.debug:
                print "ERROR, couldn't find the expected XML namespace!"
                print "Namespace parsed from XML: '" + real_ns + "'"
            raise(ImXMLError)

    def worksheet(self, pattern):
        """Look up a certain worksheet in the Excel XML tree.

        Args: pattern: the name of the worksheet

        Returns:
            worksheet: pointer to a subtree of the given etree
        """
        pattern = ".//{%s}Worksheet[@{%s}Name='%s']" % \
            (self.namespace, self.namespace, pattern)
        # we ignore broken files that contain multiple worksheets having
        # identical names and just return the first one (should be safe):
        worksheet = self.tree.findall(pattern)[0]
        if self.debug > 1: print "Found worksheet: " + str(worksheet)
        return(worksheet)

    def celldata(self, ws):
        """Provides access to the cell contents.

        Args: ws: the desired worksheet

        Automatically calls the parser if the selected worksheet
        has not yet been processed before.
        """
        if not ws in self.cells:
            self.parse_cells(ws)
        return(self.cells[ws])

    def parse_cells(self, ws):
        """Parse the cell-contents of a worksheet into a 2D array.

        After parsing the contents, they are added to the global
        map 'cells' using the worksheet name as the key.

        Args: ws: the worksheet to process
        """
        rows = self.worksheet(ws).findall('.//{%s}Row' % self.namespace)
        cells = []
        for row in rows:
            content = []
            # check if this is a header row:
            style_att = '{%s}StyleID' % self.namespace
            if style_att in row.attrib:
                # we don't process the header row, so skip it
                continue
            for cell in row:
                content.append(cell[0].text)
            if self.debug > 2:
                print str(len(row))
                print content
            cells.append(content)
        self.cells[ws] = cells
        if self.debug > 1: print self.cells
        if self.debug: print "Parsed rows: " + str(len(self.cells))

