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
# import ijpy
from microscopy import pathtools
from microscopy import dataset
from microscopy import experiment
from microscopy import fluoview
from microscopy import imagej

# NOTE: Jython doesn't allow for "relative star imports", so we NEED to do the
# import on the "olefile.py" part, we cannot use the full package (see
# http://bugs.jython.org/issue2070 and http://bugs.jython.org/issue1973 for
# more details on this bug):
import olefile

print 'Finished importing modules.'
