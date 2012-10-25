#!/usr/bin/python

"""Calculate the closest neighbor to a given spot.

Takes two Excel XML files (generated by Bitplane Imaris) with results
from the spots detection, one file containing just a single spot, the
other file containing many spots. Calculates the spot from the second
file with the closest distance to the one from the first file.
"""

# TODO:
#  - create a class for handling Excel XML, move to separate package
#  - do sanity checking
#  - evaluate datatypes from XML cells

import argparse
import sys
import numpy as np
from dist_tools import dist, dist_matrix_euclidean, find_neighbor
import imaris_xml as ix

def main():
    argparser = argparse.ArgumentParser(description=__doc__)
    argparser.add_argument('-s', '--single', required=True, type=file,
        help='Excel XML file containing a single spot.')
    argparser.add_argument('-m', '--multi', required=True, type=file,
        help='Excel XML file containing multiple spots.')
    try:
        args = argparser.parse_args()
    except IOError as e:
        argparser.error(str(e))

    tree1 = ix.parse_xml(args.single)
    myns = ix.check_namesp(tree1, 'urn:schemas-microsoft-com:office:spreadsheet')

    tree2 = ix.parse_xml(args.multi)
    myns = ix.check_namesp(tree2, 'urn:schemas-microsoft-com:office:spreadsheet')

    # we're looking for stuff in the "Position" worksheet:
    ws1_pos = ix.get_worksheet(tree1, myns, 'Position')
    ws2_pos = ix.get_worksheet(tree2, myns, 'Position')

    cells1 = ix.parse_celldata(ws1_pos[0], myns)
    cells2 = ix.parse_celldata(ws2_pos[0], myns)

    # ref_spots are taken as the base to find the closest ones
    # in the set of cand_spots
    ref_spots = ix.IMS_extract_coords(cells1)
    cand_spots = ix.IMS_extract_coords(cells2)
    dist_mat = dist_matrix_euclidean(ref_spots + cand_spots)

    ref_mask = [1] * len(ref_spots) + [0] * len(cand_spots)

    for refid, refspot in enumerate(ref_spots):
        print
        print 'Calculating closest neighbour.'
        print 'Original spot:  [' + str(refid) + ']', refspot
        nearest = find_neighbor(refid, dist_mat, ref_mask)
        print "Neighbour spot: [" + str(nearest - len(ref_spots)) + ']', \
            cand_spots[nearest - len(ref_spots)]
        print "Distance:", dist_mat[refid, nearest]
    return(0)

# see http://www.artima.com/weblogs/viewpost.jsp?thread=4829
# for this nice way to handle the sys.exit()/return() calls
if __name__ == "__main__":
    sys.exit(main())
