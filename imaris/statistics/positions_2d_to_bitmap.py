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

from imaris_xml import StatisticsSpots
import numpy as np


def parse_arguments():
    """Parse the commandline arguments."""
    argparser = argparse.ArgumentParser(description=__doc__)
    addarg = argparser.add_argument
    addarg('-i', '--infile', required=True, type=file,
           help='Imaris Excel XML export containing "Position" data.')
    addarg('-o', '--outfile', required=True, type=argparse.FileType('w'),
           help='CSV file to store the results.')
    addarg('-s', '--size', required=True, type=int,
           help='Size of generated bitmap in pixels.')
    addarg('--delta', default=50, type=int,
           help='Offset used for indicating an object (default=50).')
    addarg('--crop', action='store_const', const=True, default=False,
           help='Crop away empty regions without objects.')
    try:
        return argparser.parse_args()
    except IOError as err:
        argparser.error(str(err))


def main():
    """Read Imaris export and generate bitmap."""
    args = parse_arguments()

    spots = StatisticsSpots(args.infile)
    matrix = spots.gen_bitmap((args.size, args.size), crop=args.crop, delta=50)
    np.savetxt(args.outfile, matrix, fmt='%i')


if __name__ == "__main__":
    sys.exit(main())
