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
import argparse

import imaris_xml
import numpy as np


def parse_arguments():
    """Parse the commandline arguments."""
    argparser = argparse.ArgumentParser(description=__doc__)
    argparser.add_argument('-i', '--infile', required=True, type=file,
        help='Imaris Excel XML export containing "Position" data.')
    argparser.add_argument('-o', '--outfile', type=argparse.FileType('w'),
        help='CSV file to store the results.', required=True)
    argparser.add_argument('-s', '--size', required=True, type=int,
        help='Size of generated bitmap in pixels.')
    argparser.add_argument('-d', '--delta', default=50, type=int,
        help='Offset used for indicating an object (default=50).')
    try:
        return argparser.parse_args()
    except IOError as err:
        argparser.error(str(err))

def main():
    """Read Imaris export and generate bitmap."""
    args = parse_arguments()

    dim_x = args.size
    dim_y = dim_x

    xmldata = imaris_xml.ImarisXML(args.infile)

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
        matrix[pix_x, pix_y] += args.delta

    np.savetxt(args.outfile, matrix, fmt='%i')


if __name__ == "__main__":
    sys.exit(main())
