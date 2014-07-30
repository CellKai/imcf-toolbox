#!/usr/bin/python

"""Analyze and visualize cell junctions segmented with Imaris.

Takes a CSV file exported from Imaris via the XT/Matlab interface containing
coordinates of segmented cell junctions (via the "filaments" tool) and analyzes
them. Optionally a 3D plot can be shown interactively or exported as a series
of PNG files.
"""

import sys
import argparse

import volpy as vp
import volpy.plot as plot
from log import set_loglevel


def parse_arguments():
    """Parse the commandline arguments."""
    argparser = argparse.ArgumentParser(description=__doc__)
    argparser.add_argument('-i', '--infile', required=True, type=file,
        help='CSV file containing filament coordinates')
    argparser.add_argument('-e', '--edges', required=True, type=file,
        help='CSV file containing filament edges')
    argparser.add_argument('-o', '--outfile', type=argparse.FileType('w'),
        help='CSV file to store the results')
    argparser.add_argument('--plot', dest='plot', action='store_const',
        const=True, default=False,
        help='plot parsed filament data')
    argparser.add_argument('--export-plot', dest='export_plot', default=False,
        help='path to export PNG series of plotted filament data')
    argparser.add_argument('--showmatrix', dest='showmatrix',
        action='store_const', const=True, default=False,
        help='show the distance matrix and the longest distance pair')
    argparser.add_argument('-v', '--verbose', dest='verbosity',
        action='count', default=0)
    try:
        return argparser.parse_args()
    except IOError as err:
        argparser.error(str(err))


def main():
    """Create the junction object and do the requested tasks."""
    args = parse_arguments()
    set_loglevel(args.verbosity)

    junction = vp.CellJunction(args.infile, args.edges)

    if args.outfile:
        junction.write_output(args.outfile, args.infile)

    if args.plot or args.export_plot:
        plot.junction(junction, args.plot, args.export_plot)


if __name__ == "__main__":
    sys.exit(main())
