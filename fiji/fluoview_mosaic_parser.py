#!/usr/bin/python

import volpy.fluoview as fv
from log import log, set_loglevel
import sys
import argparse

def parse_arguments():
    """Parse commandline arguments."""
    argparser = argparse.ArgumentParser(description=__doc__)
    argparser.add_argument('--mosaic', type=file, required=True,
        help='FluoView "MATL_Mosaic.log" XML file with stage positions.')
    argparser.add_argument('-v', '--verbosity', dest='verbosity',
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

    mosaic = fv.FluoViewMosaic(args.mosaic.name)
    for i in xrange(len(mosaic.mosaics)):
        mosaic.write_tile_config(i)


if __name__ == "__main__":
    sys.exit(main())
