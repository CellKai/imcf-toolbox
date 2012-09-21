#!/usr/bin/python

# TODO:
#  - add documentation
#  - sanity/type checks

from numpy import array, linalg

def dist(p1, p2):
    point1 = array(p1)
    point2 = array(p2)
    return(linalg.norm(point1 - point2))

def largest_dist_idx(point, pointlist):
    # print point
    # print pointlist
    distances = [()] * len(pointlist)
    for i, cand in enumerate(pointlist):
        distances[i] = dist(point, cand)
    # print distances
    maxdist = max(distances)
    return([distances.index(maxdist), maxdist])

if __name__ == "__main__":
    print "This module provides just functions, no direct interface."
