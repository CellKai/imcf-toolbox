#!/bin/sh

SINGLE="../../sample_data/spots_distances/spots_green_single_ws-all.xml"
MULTI="../../sample_data/spots_distances/spots_red_multi_ws-all.xml"

./closest_neighbours.py --reference $SINGLE --candidate $MULTI > result_closest_neighbours.txt
