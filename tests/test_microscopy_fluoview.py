#!/usr/bin/python

"""Tests the volpy filament parser."""

# TODO: this is not doing any useful automated tests yet, integrate a
# run_test() function and add some useful datasets!
# For the time being, this just serves as an example how to test the modules'
# functionality.

from log import set_loglevel
import fluoview
from os.path import dirname

reload(fluoview)
set_loglevel(3)
basedir = 'TESTDATA/fluoview/'

testfile = basedir + 'minimal_1mosaic_15pct/' + 'MATL_Mosaic.log'

mosaic_exp = fluoview.FluoViewOIFMosaic(testfile)
mdc = mosaic_exp[0]
mdc.dim
mdc.get_overlap()
mdc.storage
oifds = mdc.subvol[3]
oifds.get_dimensions()
oifds.position
oifds.storage

