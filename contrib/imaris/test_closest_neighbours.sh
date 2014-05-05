#!/bin/sh

BASEDIR="TESTDATA/spots_distances"
REFS="${BASEDIR}/spots_green_single_ws-all.xml"
CAND="${BASEDIR}/spots_red_multi_ws-all.xml"

RES="${BASEDIR}/result_closest_neighbours.txt"

./closest_neighbours.py --reference $REFS --candidate $CAND 2> $RES
