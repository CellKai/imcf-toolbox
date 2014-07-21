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

    sec_size = int(sheet.cell_value(1,8))
    sections = int(sheet.nrows / (sec_size + 3))
    print("Section size: %s, number of sections: %s" % (sec_size, sections))

    # now we assemble the data in a numpy array that can easily be exported
    # using numpy's savetxt() function
    assembly = np.zeros(shape = (sec_size, sections + 3))
    assembly[:, 0] = sheet.col_values(0, 3, 3 + sec_size)
    assembly[:, 1] = sheet.col_values(1, 3, 3 + sec_size)
    # assembly[:, 2] <-- we need to calculate the euclidean deltas here

    col = 3
    for sec in range(sections / 2):
        start = (sec_size + 3) * sec + 3
        # print start
        assembly[:, col] = sheet.col_values(2, start, start + sec_size)
        col += 1
        start += (sec_size + 3) * (sections / 2)
        # print start
        assembly[:, col] = sheet.col_values(2, start, start + sec_size)
        col += 1

    print assembly


if __name__ == "__main__":
    sys.exit(main())
