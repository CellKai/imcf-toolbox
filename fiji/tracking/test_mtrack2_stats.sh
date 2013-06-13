#!/bin/sh

BASEDIR="TESTDATA/mtrack2"

for infile in $(ls $BASEDIR/*.txt) ; do
    fname=$(basename $infile)
    outfile="results__$(echo $fname | sed 's,\.txt$,.csv,')"
    ./mtrack2_stats.py --infile $BASEDIR/$fname --outfile $BASEDIR/$outfile
done
