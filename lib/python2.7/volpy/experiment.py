#!/usr/bin/python

"""Tools to process microscopy experiment data."""

from os import sep
# from os.path import basename, dirname, join, exists
from os.path import basename, dirname
from log import log
# from misc import readtxt, flatten
# from volpy import dataset


class Experiment(list):

    """Generic class for microscopy experiment data."""

    def __init__(self, infile):
        """Set up the common experiment properties.

        Parameters
        ----------
        infile : str
            The experiment file or folder.

        Instance Variables
        ------------------
        infile : {'path': str,    # full path to input file
                  'dname': str,   # the directory name (last part of 'path')
                  'fname': str    # the input *file*name
                 }
        datasets : list(Dataset)
        """
        super(Experiment, self).__init__()
        log.debug("Creating an 'Experiment' object.")
        self.infile = {'dname': '', 'fname': '', 'path': ''}
        self.infile['path'] = dirname(infile).replace('\\', sep)
        self.infile['dname'] = basename(self.infile['path'])
        self.infile['fname'] = basename(infile)
        log.debug(self.infile)
        self.datasets = list()

    def add_dataset(self, dset):
        """Add a dataset to this experiment."""
        log.debug("Adding a dataset.")
        self.datasets.append(dset)
