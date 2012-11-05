#!/bin/sh

TILES="tiles.csv"
SRC="unaligned.xuv"
TGT="result_realigned.xuv"

# file to hold the messages sent to stdout:
OUT="output_test_process-tilegrid.txt"

./process-tilegrid.py --tiles $TILES --infile $SRC --outfile $TGT --overlap 0.15 > $OUT
