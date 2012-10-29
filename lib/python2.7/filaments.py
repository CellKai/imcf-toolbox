#!/usr/bin/python

import csv
from dist_tools import dist_matrix_euclidean, get_max_dist_pair, \
    sort_neighbors, build_filament_mask, elastic_bands


class Filament(object):
    '''Builds connected components ("filaments") from a given set of
    coordinates in space that are read from a CSV file.
    '''

    def __init__(self, csvfile, debug=0):
        self.debug = debug
        self.filament = []
        self.parse_float_tuples(csvfile)

    def parse_float_tuples(self, fname):
        """Parses every line of a CSV file into a tuple.

        Parses a CSV file, makes sure all the parsed elements are float
        values and assembles a 2D list of them, each element of the list
        being a n-tuple holding the values of a single line from the CSV.

        Args:
            fname: A filename of a CSV file.

        Returns:
            A list of n-tuples, one tuple for each line in the CSV, for
            example:

            [[1.3, 2.7, 4.22], [22.5, 3.2, 5.5], [2.2, 8.3, 7.6]]

        Raises:
            ValueError: The parser found a non-float element in the CSV.
        """
        # print fname
        parsedata = csv.reader(fname, delimiter=',', quoting=csv.QUOTE_NONNUMERIC)
        # print parsedata
        for row in parsedata:
            # print 'current row: ' + str(row)
            num_val = []
            for val in row:
                # print val
                num_val.append(val)
            self.filament.append(num_val)
        if self.debug > 1: print self.filament
        if self.debug:
            print 'Parsed ' + str(len(self.filament)) + ' points from file.'
