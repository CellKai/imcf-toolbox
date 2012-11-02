#!/bin/sh

REFS="__testdata/spots_green_single_ws-all.xml"
CAND="__testdata/spots_red_multi_ws-all.xml"

RES="result_closest_neighbours.txt"

./closest_neighbours.py --reference $REFS --candidate $CAND --outfile $RES
