#!/bin/sh

REFS="__testdata/spots_green_single_ws-all.xml"
CAND="__testdata/spots_red_multi_ws-all.xml"

./closest_neighbours.py --reference $REFS --candidate $CAND > result_closest_neighbours.txt
