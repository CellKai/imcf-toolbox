#!/bin/sh

INFILE="TESTDATA/spots_distances/spots_nocorners_ws-all.xml"
PREFIX="TESTDATA/spots_distances/spots_nocorners_bitmap"
set -x
./spots_to_bitmap.py --size 256 -i $INFILE -o ${PREFIX}-cropped.csv --crop
./spots_to_bitmap.py --size 256 -i $INFILE -o ${PREFIX}-uncropped.csv 
set +x

INFILE="TESTDATA/spots_distances/spots_allcorners_ws-all.xml"
PREFIX="TESTDATA/spots_distances/spots_allcorners_bitmap"
set -x
./spots_to_bitmap.py --size 256 -i $INFILE -o ${PREFIX}-cropped.csv --crop
./spots_to_bitmap.py --size 256 -i $INFILE -o ${PREFIX}-uncropped.csv 
set +x
