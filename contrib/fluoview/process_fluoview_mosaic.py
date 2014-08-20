#!/usr/bin/python

"""Parse a FluoView project file and generate code for ImageJ's stitcher."""

import volpy.fluoview as fv
from log import set_loglevel
import sys
import argparse
from os.path import dirname, basename


def parse_arguments():
    """Parse commandline arguments."""
    argparser = argparse.ArgumentParser(description=__doc__)
    add = argparser.add_argument
    add('--mosaic', type=file, required=True,
        help='FluoView "MATL_Mosaic.log" XML file with stage positions.')
    add('--out', type=str, required=False, default='',
        help='Output directory, otherwise the input directory is used.')
    add('-f', '--fixsep', action='store_const', const=True, default=False,
        help='Adjust path separators to current environment.')
    add('-v', '--verbosity', dest='verbosity',
        action='count', default=0)
    try:
        args = argparser.parse_args()
    except IOError as err:
        argparser.error(str(err))
    return args


def main():
    """Parse commandline arguments and run parser."""
    args = parse_arguments()
    set_loglevel(args.verbosity)

    dname = dirname(args.mosaic.name)
    fname = basename(args.mosaic.name)
    if args.out == '':
        dout = dname
    else:
        dout = args.out

    mosaic = fv.FluoViewMosaic(args.mosaic.name)
    mosaic.write_all_tile_configs(path=dout, fixpath=args.fixsep)
    code = mosaic.gen_stitching_macro_code('stitching', path=dname)
    mosaic.write_stitching_macro(code, dname=dout)


if __name__ == "__main__":
    sys.exit(main())
