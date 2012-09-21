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

from scipy import reshape, sqrt
from numpy.matlib import repmat, repeat, sum
def dist_matrix_euclidean(points):
    num_points = len(points)
    # print len(repmat(points, num_points, 1))
    # print len(repeat(points, num_points, axis=0))
    dist_mat = sqrt(sum((repmat(points, num_points, 1) -
                        repeat(points, num_points, axis=0))**2, axis=1))
    return dist_mat.reshape((num_points, num_points))


if __name__ == "__main__":
    print "This module provides just functions, no direct interface."
