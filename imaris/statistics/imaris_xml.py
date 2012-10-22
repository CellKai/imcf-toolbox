#!/usr/bin/python

# TODO:

import xml.etree.ElementTree as etree
import sys

def parse_xml(infile):
    """Aux function to call the etree parser.

    Just an auxiliary function for debugging statements.
    """
    print "Processing file: " + infile.name
    tree = etree.parse(infile)
    # print "Done parsing the XML."
    # print
    return(tree)

def check_namesp(xml_etree, expected_ns):
    """Check if an XML tree has a certain namespace.

    Takes an XML etree object and a string denoting the expected
    namespace, checks if the namespace of the XML tree matches.
    Returns the namespace if yes, exits otherwise.
    """
    # FIXME: throw an exception or return false instead of exiting
    real_ns = xml_etree.getroot().tag[1:].split("}")[0]
    if not real_ns == expected_ns:
        print "ERROR, this file doesn't have the expected XML namespace!"
        sys.exit(1)
    # print "Namespace parsed from XML document: '" + real_ns + "'"
    # print
    return(real_ns)

def get_worksheet(xml_etree, ns, pattern):
    """Look up a certain worksheet in an Excel XML tree.

    Args:
        xml_etree: etree object
        ns: the XML namespace to use for searching
        pattern: the name of the worksheet

    Returns:
        worksheet: pointer to a subtree of the given etree
    """
    # FIXME: what happens if the worksheet can't be found??
    pattern = ".//{%s}Worksheet[@{%s}Name='%s']" % (ns, ns, pattern)
    worksheet = xml_etree.findall(pattern)
    return(worksheet)

def parse_celldata(worksheet, ns):
    """Parse the cell-contents of a worksheet into a 2D array.

    Args:
        worksheet: the worksheet to process
        ns: the XML namespace

    Returns:
        cells: a 2D array of the form (r=row, c=column):
               [ [r1c1, r1c2, r1c3, ...],
                 [r2c1, r2c2, r2c3, ...],
                 [r3c1, r3c2, r3c3, ...],
                 ...                      ]
    """
    # TODO: error handling
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
    # print "Parsed rows: " + str(len(cells))
    return(cells)

def IMS_extract_coords(table_cells):
    """Extract Imaris-style coordinates and ID's from a cell array.

    Args:
        table_cells: 2D array with the cell contents of a worksheet.

    Returns:
        coords: array using the ID as index, storing 3-tuples of floats
                representing the coordinates in (x, y, z) order.
    """
    coords = []
    # extract positions and ID:
    for cell in table_cells:
        id = int(cell[7])
        x = float(cell[0])
        y = float(cell[1])
        z = float(cell[2])
        coords.insert(id, (x, y, z))
    # print "Parsed coordinates:", str(len(coords))
    return(coords)


if __name__ == "__main__":
    print "This module provides just functions, no direct interface."
