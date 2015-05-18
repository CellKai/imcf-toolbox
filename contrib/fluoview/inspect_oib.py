#!/usr/bin/python

"""Tool to inspect OIB files produced with Olympus FluoView.

Olympus OIB is a container file type using the Microsoft OLE2 format and can
usually be extracted using 7-Zip. This tool tries to parse an OIB file and
read the description file 'OibInfo.txt' from the topmost hierarchy level.
"""

import sys
import argparse
import olefile
import codecs
from log import log, set_loglevel

def parse_arguments():
    """Parse commandline arguments."""
    argparser = argparse.ArgumentParser(description=__doc__)
    add = argparser.add_argument
    add('--oib', type=file, required=True,
        help='FluoView OIB file.')
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

    log.debug("Using 'olefile' version %s (%s)." %
             (olefile.__version__, olefile.__date__))

    ole = olefile.OleFileIO(args.oib)
    stream = ole.openstream(['OibInfo.txt'])
    # stream = ole.openstream(['Storage00001', 'Stream00060'])
    conv = codecs.decode(stream.read(), 'utf16')
    log.warn(conv)


if __name__ == "__main__":
    sys.exit(main())
