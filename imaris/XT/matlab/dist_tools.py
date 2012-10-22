#!/usr/bin/python

# TODO:
#  - add documentation
#  - sanity/type checks
#  - rename into filament_tools?

import math
def calc_dist_xyz(p1, p2):
    """Calculates the euclidean distance between two points in 3D.

    Args:
        p1, p2: lists with 3 numerical elements each

    Returns:
        dist: float containing euclidean distance
    """
    dx = abs(p2[0] - p1[0])
    dy = abs(p2[1] - p1[1])
    dz = abs(p2[2] - p1[2])
    dist = math.sqrt(dx**2 + dy**2 + dz**2)
    return(dist)

from numpy import array, linalg
def dist(p1, p2):
    """Calculates the euclidean distance of two points (N dimensional).

    Args:
        p1, p2: lists with an equal nr of numerical elements

    Returns:
        dist: float containing euclidean distance
    """
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
from numpy.matlib import repmat, repeat, sum, where
def dist_matrix_euclidean(points):
    num_points = len(points)
    # print len(repmat(points, num_points, 1))
    # print len(repeat(points, num_points, axis=0))
    dist_mat = sqrt(sum((repmat(points, num_points, 1) -
                        repeat(points, num_points, axis=0))**2, axis=1))
    return dist_mat.reshape((num_points, num_points))

def get_max_dist_pair(matrix):
    # Takes a distance matrix and finds the pair having the largest
    # distance to each other. Returns a tuple of index numbers.
    maxdist = 0
    pair = (-1, -1)
    for row_num, row in enumerate(matrix):
        row_max = max(row)
        if row_max > maxdist:
            maxdist = row_max
            max_pos = where(row == row_max)[0][0]
            pair = (row_num, max_pos)
            # print [row_num] + [where(row == row_max)[0][0]] + [maxdist]
            # print pair
    return pair

from numpy import ma
def find_neighbor(pid, dist_mat, mask):
    """Finds the closest neighbor in a given distance matrix.

    Takes a reference point and looks up the closest neighbor in a
    masked distance matrix. The mask can be used to exclude selected
    points in the calculation, for example when they have already been
    processed earlier. Otherwise use a 0-mask.

    Args:
        pid: the index of the reference point
        dist_mat: the euclidean distance matrix of all points
        mask: binary array to use as a mask

    Returns:
        closest: index of the closest neighbor
    """
    masked_dists = ma.array(dist_mat[pid], mask=mask)
    closest = masked_dists.argmin()
    return closest

def sort_neighbors(dist_mat, coords):
    """Sorts a list of indices to minimize the distance between elements.

    Takes a euclidean distance matrix and an array of coordinates and
    iteratively builds a list of indices where each point is followed
    by its closest neighbor, starting at point 0 of the coordinates list.

    Args:
        dist_mat: the euclidean distance matrix of all points
        coords: the list of coordinates

    Returns:
        adjacents: list of indices in sorted order
    """
    adjacents = []

    # inital mask is 0 everywhere (no masking at all):
    mask = [0] * len(dist_mat[0])

    # for convenience we use a set instead of a list, so we don't have
    # to care on what position the current element is
    pointset = set(range(len(coords)))
    cur = 0
    while len(pointset) > 0:
        adjacents.append(cur)
        pointset.remove(cur)
        mask[cur] = 1
        closest = find_neighbor(cur, dist_mat, mask)
        # print str(cur) + ' - ' + str(closest)
        cur = closest
    return adjacents

def build_filament_mask(adjacent, delimiters):
    mask = [True] * len(adjacent)
    mask_adj = [True] * len(adjacent)
    maskval = True
    # required to determine which delimiter is found first:
    found_first = False
    # if second comes first, we need to invert the mask eventually:
    invert = False
    for i, point in enumerate(adjacent):
        if point == delimiters[0]:
            found_first = True
            maskval = not(maskval)
        if point == delimiters[1]:
            maskval = not(maskval)
            # check if we need to invert the mask:
            if not(found_first): invert = True
        mask[point] = maskval
        mask_adj[i] = maskval
    if invert:
        # print 'inverting mask.'
        mask = [ not(x) for x in mask ]
        mask_adj = [ not(x) for x in mask_adj ]
    # print mask
    return (mask, mask_adj)

def elastic_bands(pl1, pl2, mask1, mask2, dist_mat):
    """Calculates minimal connections between two filament pointsets.

    Takes two pointlists (the filaments), the corresponding masks, and a
    distance matrix. Iterates over the pointlists and calculates the
    closest point from the other set (think of elastic bands of minimal
    energy connecting them, hence the name). Builds a set of tuples
    representing the bands of the form (id1, id2) where id1 < id2 to make
    sure we don't add "inverted" duplicates.

    Args:
        pl1, pl2: pointlists (ids of points)
        mask1, mask2: corresponding array masks
        dist_mat: euclidean distance matrix

    Returns:
        bands: a set of tuples (id_a, id_b) where id_a < id_b
    """
    bands = set()
    for cur in pl1:
        neigh = find_neighbor(cur, dist_mat, mask2)
        if cur < neigh:
            bands.add((cur, neigh))
        else:
            bands.add((neigh, cur))
    for cur in pl2:
        neigh = find_neighbor(cur, dist_mat, mask1)
        if cur < neigh:
            bands.add((cur, neigh))
        else:
            bands.add((neigh, cur))
    # print bands
    return bands


if __name__ == "__main__":
    print "This module provides just functions, no direct interface."
