#!/usr/bin/python

from xlrd import open_workbook, colname
import numpy as np
import argparse
import sys


def parse_arguments():
    """Parse commandline arguments."""
    argparser = argparse.ArgumentParser(description=__doc__)
    argparser.add_argument('--infile', required=True, type=str,
        help='Metamorph Excel export file.')
    argparser.add_argument('-v', '--verbosity', dest='verbosity',
        action='count', default=0)
    try:
        args = argparser.parse_args()
    except IOError as err:
        argparser.error(str(err))
    return args

def main():
    """Parse commandline arguments and run reader."""
    args = parse_arguments()

    xlfile = open(args.infile,'rb').read()
    wb = open_workbook(file_contents=xlfile)

    sheet = wb.sheet_by_index(0)
    print("Sheet 0 name: %s" % sheet.name)

    # sec_size = 83
    sec_size = int(sheet.cell_value(1,8))
    sections = int(sheet.nrows / (sec_size + 3))
    print("Section size: %s, number of sections: %s" % (sec_size, sections))

    for sec in range(sections):
        print sheet.row_values(1,1)


if __name__ == "__main__":
    sys.exit(main())
