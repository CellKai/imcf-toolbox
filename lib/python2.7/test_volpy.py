#!/usr/bin/python

'''Test script for the "volpy" module.'''

from csvtools import parse_float_tuples;
from volpy import dist_matrix_euclidean;
import argparse
import pprint

argparser = argparse.ArgumentParser(description=__doc__)
argparser.add_argument('-i', '--infile', required=True, type=file,
    help='CSV file containing filament coordinates')
# use redirection for the moment, so disable 'outfile'
# argparser.add_argument('-o', '--outfile', required=True, type=file,
#     help='file to place results in')
try:
    args = argparser.parse_args()
except IOError as e:
    argparser.error(str(e))

tuples_list = parse_float_tuples(args.infile)
distance_matrix = dist_matrix_euclidean(tuples_list)

pp = pprint.PrettyPrinter(indent=4)
pp.pprint(distance_matrix)
