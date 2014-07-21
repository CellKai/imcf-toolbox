#!/bin/sh

BASEDIR="TESTDATA"
TILES="${BASEDIR}/tiles.csv"
SRC="${BASEDIR}/unaligned.xuv"
TGT="${BASEDIR}/result_realigned.xuv"

# file to hold the messages sent to stdout:
OUT="${BASEDIR}/output_test_process-tilegrid.txt"

./process-tilegrid.py --tiles $TILES --infile $SRC --outfile $TGT --overlap 0.15 > $OUT
