"""Wrapper script to trigger bytecode generation from within Jython.

This script doesn't do anything except for importing all packages and their
individual sub-modules to trigger the compilation of bytecode from Jython.
"""

import sys
import os.path

cwd = os.path.realpath('src/')
sys.path.insert(0, cwd)

print 'Current sys.path settings:'
for path in sys.path:
    print path

import log
import misc
import imcf
import microscopy
import ijpy
from microscopy import pathtools
from microscopy import dataset
from microscopy import experiment
from microscopy import fluoview
from microscopy import imagej

print 'Finished importing modules.'
