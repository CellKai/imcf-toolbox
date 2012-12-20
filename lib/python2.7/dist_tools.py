#!/usr/bin/python

# TODO:
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
    """Find the point with the largest distance to a marked point.

    Takes a point (euclidean coordinates) and a list of points,
    calculates the distance of the single point to all points in the
    list and returns the index and the distance of the marked one.

    Args:
        point: n-tuple of euclidean coordinates
        pointlist: list of n-tuples of euclidean coordinates

    Returns:
        [index, distance]: integer with index, float with distance
    """
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
def dist_matrix_euclidean(pts):
    """Calculates the euclidean distance matrix for a set of points.

    Args:
        pts: a list of n-dimensional coordinates, e.g.
             pts = [ [1, 2], [4, 6] ]

    Details:
    Uses two auxiliary matrixes to easily calculate the distance from
    each point to every other point in the list using this approach:
    (1) aux matrixes:
    repmat(l, n1, n2): l is repeated n1 times, along axis 1, and n2
        times along axis 2, so repmat(pts, len(pts), 1) =
        array( [ [1, 2], [4, 6], [1, 2], [4, 6] ] )
    repeat(l, n, a): each element of l is repeated n times along axis a
        (w/o 'a' a plain list is generated), so repeat(pts, 2, 1) =
        array( [ [1, 2], [1, 2], [4, 6], [4, 6] ] )
    (2) Pythagoras:
    Then, the element-wise difference of the generated matrixes is
        calculated each value is squared:
        array( [ [ 0,  0], [ 9, 16], [ 9, 16], [ 0,  0] ] )
    These squares are then summed up (linewise) using sum(..., axis=1):
        array([ 0, 25, 25,  0])
    Finally the square root is taken for each element:
        array([ 0.,  5.,  5.,  0.])

    Returns:
        To transform the list into a distance matrix, we use reshape():
        array( [ [ 0.,  5.],
                 [ 5.,  0.] ] )
    """
    dist_mat = sqrt(
                    sum(
                           (
                               repmat(pts, len(pts), 1) -
                               repeat(pts, len(pts), axis=0)
                           )**2,
                           axis=1
                       )
                   )
    return dist_mat.reshape((len(pts), len(pts)))

def get_max_dist_pair(matrix):
    """Determine points with largest distance using a distance matrix.

    Args:
        matrix: euclidean distance matrix

    Returns:
        (i1, i2): tuple of index numbers of the largest distance pair.
    """
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

def path_greedy(dist_mat, mask_ref, pair):
    """Uses greedy search to find a path between a pair of points.

    Takes a euclidean distance matrix, a mask and a tuple denoting the start
    and stop index, calculates a path from first to last using the greedy
    approach by always taking the closest element next that has not yet been
    processed.

    Args:
        dist_mat: the euclidean distance matrix of all points
        mask_ref: array mask (a binary list)
        pair: tuple of index numbers for dist_mat

    Returns: (sequence, mask)
        sequence: list of indices denoting the greedy path
        mask: the mask of the above sequence
    """
    sequence = []

    # 'list' is a mutable type, so we explicitly copy it and return a new
    # mask at the end, to avoid silently modifying the reference (bad style)
    mask = mask_ref[:]
    # make sure the end point is unmasked, otherwise we'll loop endlessly:
    mask[pair[1]] = 0

    cur = pair[0]
    while True:
        sequence.append(cur)
        mask[cur] = 1
        closest = find_neighbor(cur, dist_mat, mask)
        if closest == pair[1]:
            sequence.append(pair[1])
            mask[closest] = 1
            break
        cur = closest
    # print 'path (%s->%s): %s' % (pair[0], pair[1], sequence)
    return (sequence, mask)

def remove_first_last(pointlist):
    # copy the pointlist
    cropped = pointlist[:]
    cropped.pop()
    cropped.reverse()
    cropped.pop()
    cropped.reverse()
    return cropped

def sort_neighbors(dist_mat):
    """Sorts a list of indices to minimize the distance between elements.

    Takes a euclidean distance matrix and iteratively builds a list of
    indices where each point is followed by its closest neighbor, starting at
    point 0 of the distance matrix.

    Args:
        dist_mat: the euclidean distance matrix of all points

    Returns:
        adjacents: list of indices in sorted order
    """
    adjacents = []

    # inital mask is 0 everywhere (no masking at all):
    mask = [0] * len(dist_mat[0])

    # for convenience we use a set instead of a list, so we don't have
    # to care on what position the current element is
    pointset = set(range(len(dist_mat[0])))
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
    """Calculates filament masks for distance matrix and adjacency lists.

    Takes an ordered list of indices (adjacency list) and a tuple of
    delimiters marking the first and the last index of the adjacency
    list that belongs to this filament.

    Calculates two arrays masking the entries that don't belong to the
    filament denoted this way, the first mask uses the numbers given
    in the adjacency list (to be used with the distance matrix), the
    second mask uses the index positions of the list (for usage with
    the adjacency list itself).

    Args:
        adjacent: adjacency list of the filament
        delimiters: index numbers of first and last filament entry

    Returns:
        (dist_mat_mask, adjacent_mask): tuple of masks
    """
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

def elastic_bands(pl1, mask2, dist_mat):
    """Calculates minimal connections between two filament pointsets.

    FIXME: update documentation, the mask is masking the points in the
    distance matrix that are not in pointlist now!

    Takes two pointlists (the filaments), the corresponding masks, and a
    distance matrix. Iterates over the pointlists and calculates the
    closest point from the other set (think of elastic bands of minimal
    energy connecting them, hence the name). Builds a set of tuples
    representing the bands of the form (id1, id2) where id1 < id2 to make
    sure we don't add "inverted" duplicates.

    Args:
        pl1: pointlist (ids of points)
        mask2: corresponding array mask
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
    return bands

def gen_mask(pointlist, masklength):
    """Generates a binary mask given by a list of indices.

    Takes a list of indices and a length parameter, generates a mask with
    that given length, masking the indices in the given list.
    """
    mask = [0] * masklength
    for point in pointlist:
        mask[point] = 1
    return mask

def gen_unmask(pointlist, masklength):
    """Generates a binary mask given by a list of indices.

    Takes a list of indices and a length parameter, generates a mask with
    that given length, masking everything but the indices in the given list.
    """
    mask = [1] * masklength
    for point in pointlist:
        mask[point] = 0
    return mask

def tesselate(pl1, pl2, dist_mat):
    """Calculates a polygonal partition of a surface in space.

    Takes a distance matrix and two lists of indices (describing sequences
    of points, e.g. filament-like structures) that can be thought of the
    border or rim of an object in space. The two index-lists are required to
    have the same start and end point. The function calculates a partition
    of this object into triangles (tesselation), trying to minimize the
    overall area of all triangles.

    Args:
        pl1, pl2: pointlists (ids of points)
        dist_mat: euclidean distance matrix

    Returns:
        edges: list of tuples with index numbers denoting the edges
    """
    edges = []

    pl1_len = len(pl1)
    pl2_len = len(pl2)

    # make sure the pointlists are connected:
    if not pl1[0] == pl2[0]:
        raise(Exception)
    if not pl1[pl1_len - 1] == pl2[pl2_len - 1]:
        raise(Exception)

    # first we need to create the masks:
    mask1 = gen_mask(pl1, len(dist_mat[0]))
    mask2 = gen_mask(pl2, len(dist_mat[0]))
    # print "%s\n%s\n%s\n%s" % (pl1, mask1, pl2, mask2)

    i2 = 1
    for i1, cur in enumerate(pl1):
        opp_cur = find_neighbor(cur, dist_mat, mask1)
        edges.append((cur, opp_cur))
        # print "-- edgelist: %s" % edges

        # if the next point is the last one, we're done:
        # FIXME: check if pl2 is empty then!!
        if i1 + 1 == pl1_len:
            break

        nxt = pl1[i1 + 1]
        opp_nxt = find_neighbor(nxt, dist_mat, mask1)
        # print "next: (%s, %s)" % (nxt, opp_nxt)

        # if the next point has the same opponent as the current one,
        # we don't need to care of anything now nor adjust the pointer
        # of 'i2', so we just go on to that next point:
        if opp_nxt == opp_cur:
            continue

        # we have to look for missing points:
        missing = []
        while i2 < pl2_len:
            i2 += 1
            # print "i2: %s" % i2
            # stop when reaching the opponent of the next point:
            if pl2[i2] == opp_nxt:
                break
            # otherwise it is one of the points we're looking for:
            missing.append(i2)

        # now we generate edges for missing points, first by creating
        # a temporary mask covering everything but the current and the
        # next point in our list:
        tmp_mask = [1] * len(dist_mat[0])
        tmp_mask[cur] = 0
        tmp_mask[nxt] = 0
        # print "missing points: %s\ntmp_mask: %s" % (missing, tmp_mask)
        for point in missing:
            tmp_opp = find_neighbor(pl2[point], dist_mat, tmp_mask)
            edges.append((tmp_opp, pl2[point]))
            # print "-- edgelist: %s" % edges

        # print "next opponent: pl2[%s] = %s" % (i2, pl2[i2])

    # print "edges: %s" % edges
    return edges

if __name__ == "__main__":
    print "This module provides just functions, no direct interface."
