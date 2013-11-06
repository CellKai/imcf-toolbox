#!/usr/bin/python
# coding: utf-8

"""Generate a bitmap from coordinates given as an Imaris Excel XML export.

Takes a XML file exported from Imaris via the statistics tab containing
coordinates of segmented objects and uses them to generate a 2D bitmap of a
given size. The resulting bitmap is stored as a CSV file that can be used in
ImageJ via the File>Import>Text_Image function, empty pixels are black, the
others contain values > 0.
"""

import sys

import imaris_xml
import numpy as np

def main():
    """Read Imaris export and generate bitmap."""
    # TODO: use arg
    dim_x = 256
    dim_y = dim_x
    offset = 50

    # TODO: use arg
    fh = open('spots_red_multi_ws-all.xml', 'r')
    xmldata = imaris_xml.ImarisXML(fh)

    coords = xmldata.coordinates('Position')
    coords_2d = coords[:,0:2]

    # TODO: make this configurable
    # remove emtpy blocks (aka shift coords to origin)
    coords_2d[:,0] -= coords_2d[:,0].min()
    coords_2d[:,1] -= coords_2d[:,1].min()

    xmax = coords_2d[:,0].max()
    ymax = coords_2d[:,1].max()

    matrix = np.zeros((dim_x, dim_y), dtype=np.int)
    for point in coords_2d:
        pix_x = int((point[0] / xmax) * (dim_x - 1))
        pix_y = int((point[1] / ymax) * (dim_y - 1))
        # print "(%f,%f) -> (%i,%i)" % (point[0], point[1], pix_x, pix_y)
        matrix[pix_x, pix_y] += offset

    # TODO: use arg
    np.savetxt('bitmap.csv', matrix, fmt='%i')


if __name__ == "__main__":
    sys.exit(main())
