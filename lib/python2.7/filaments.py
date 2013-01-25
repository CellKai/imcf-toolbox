#!/usr/bin/python

from volpy import *
from numpy import loadtxt

class Filament(object):
    '''Builds connected components ("filaments") from a given set of
    coordinates in space that are read from a CSV file.
    '''

    def __init__(self, csvfile, debug=0):
        self.debug = debug
        self.filament = []
        # loadtxt() expects floats (or it complains), returns an ndarray()
        self.data = loadtxt(csvfile, delimiter=',')
        if self.debug > 0:
            print 'Parsed %i points from CSV.\n%s' % \
                (len(self.data), str(self.data))

