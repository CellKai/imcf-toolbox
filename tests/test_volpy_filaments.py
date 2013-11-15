#!/usr/bin/python

"""Tests the volpy filament parser."""

from volpy import Filament
from log import set_loglevel, set_filehandler


def run_test(fin, fout):
    flmnt = Filament(fin)

    output = open(fout, 'w')
    output.write(str(flmnt.get_coords()))
    print 'Parsed %i points from "%s"' % \
        (len(flmnt.get_coords()), fin)
    print('Written results to "%s"' % fout)

set_filehandler('/tmp/asdfasdfasdf', no_stdout=True)
set_loglevel(2)
basedir = 'TESTDATA/filaments/'

infile = basedir + 'testdata-filaments-small.csv'
outfile = basedir + 'result_filaments-small.coords.txt'
run_test(infile, outfile)

infile = basedir + 'testdata-filaments-manual.csv'
outfile = basedir + 'result_filaments-manual.coords.txt'
run_test(infile, outfile)

infile = basedir + 'testdata-junction-wt-001.csv'
outfile = basedir + 'result_junction-wt-001.coords.txt'
run_test(infile, outfile)
