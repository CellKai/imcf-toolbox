#!/usr/bin/python

"""Tools to process microscopy experiment data."""

from log import log
# from misc import readtxt, flatten
# from volpy import dataset
from volpy.pathtools import parse_path


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
        self.infile = parse_path(infile)
        log.warn(self.infile)

    def add_dataset(self, dset):
        """Add a dataset to this experiment."""
        log.debug("Adding a dataset.")
        self.append(dset)
