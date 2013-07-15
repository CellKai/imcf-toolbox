#!/usr/bin/python

"""Discrete volumetric data tools.

Provides distance, area, mesh-related calculations on spots
in three dimensional space.
"""

from log import log
from scipy import reshape, sqrt
from numpy import cross, linalg, ma
import numpy as np
import math
from numpy.matlib import repmat, repeat, sum, where

# TODO:

# - consolidate the np.function vs "from numpy import ..." usage
# - join the "filaments" module with this one, extend the Filament class to
#   be able to return the distance matrix, the masks of the individual
#   filaments, access to start and end points, etc.
# - consolidate docstrings format
# - sanity/type checks

__all__ = [
    'build_filament_mask',
    'build_tuple_seq',
    'dist_matrix',
    'get_max_dist_pair',
    'path_greedy',
    'sort_neighbors',
    'tri_area',
    'tesselate',
    # 'find_neighbor',
    # 'gen_mask',
    # 'gen_unmask',
]

# def dist(p1, p2) ### REMOVED ###
# if there is really a shortcut required for calculating the norm, this can
# easily be done via a lambda function:
# d = lambda p1, p2: linalg.norm(p1 - p2)


def dist_matrix(pts):
    """Calculate the euclidean distance matrix (EDM) for a set of points.

    Args:
        pts: a two-dimensional numpy.ndarray, e.g.
             pts = array([-1.0399, -0.594 , -0.54  ])
             or a list of n-dimensional coordinates, e.g.
             pts = [ [1, 2], [4, 6] ]

    Returns: the distance matrix as 2d ndarray, e.g.
        array( [ [ 0.,  5.],
                 [ 5.,  0.] ] )
    """
    """
    Implementation Details:
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
    To transform the list into a distance matrix reshape() is used.
    """
    dist_mat = sqrt(
                    sum(
                           (
                               repmat(pts, len(pts), 1) -
                               repeat(pts, len(pts), axis=0)
                           ) ** 2,
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
    # FIXME: this can be done with argmax()!
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
    processed. Processed points will be disabled in the mask.

    Args:
        dist_mat: the euclidean distance matrix of all points
        mask_ref: array mask (a binary list) or 'None'
        pair: tuple of index numbers for dist_mat

    Returns: (sequence, mask)
        sequence: list of indices denoting the greedy path
        mask: the mask of the above sequence
        plen: the overall length of the path
    """
    sequence = []
    plen = 0

    if mask_ref is None:
        # create an empty mask with the number of points:
        mask = [0] * len(dist_mat[0])
    else:
        # 'list' is a mutable type, so we explicitly copy it and return a new
        # mask at the end, to avoid silently modifying the reference
        mask = mask_ref[:]

    # make sure the end point is unmasked, otherwise we'll loop endlessly:
    mask[pair[1]] = 0

    cur = pair[0]
    while True:
        sequence.append(cur)
        mask[cur] = 1
        closest = find_neighbor(cur, dist_mat, mask)
        plen += dist_mat[cur, closest]
        log.debug('accumulated path length: %s' % plen)
        if closest == pair[1]:
            sequence.append(pair[1])
            mask[closest] = 1
            break
        cur = closest
    log.info('path length: %s' % plen)
    log.info('path (%s->%s): %s' % (pair[0], pair[1], sequence))
    return (sequence, mask, plen)


def cut_extrema(lst):
    """Returns the first & last element and the rest of a list (copied)."""
    # initialize
    first = []
    last = []
    # copy the list
    listcopy = lst[:]
    if len(lst) > 0:
        first = listcopy.pop(0)
    if len(lst) > 0:
        last = listcopy.pop(-1)
    return (first, last, listcopy)


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
            if not(found_first):
                invert = True
        mask[point] = maskval
        mask_adj[i] = maskval
    if invert:
        # print 'inverting mask.'
        mask = [not(x) for x in mask]
        mask_adj = [not(x) for x in mask_adj]
    # print mask
    return (mask, mask_adj)


def build_tuple_seq(sequence, cyclic=False):
    """Convert a sequence into a list of 2-tuples.

    Takes a sequence (list) and returns a list of 2-tuples where
    each tuple consists of the previous list entry and the current one,
    starting with the entry (last, 1st), then (1st, 2nd) and so on.

    The optional parameter "cyclic" states whether the sequnce should
    by cyclic or acyclic, meaning the last and the first element will
    be connected or not.
    """
    # TODO: check if this could be done using a clever lambda function
    # print sequence
    tuples = []
    for i, elt in enumerate(sequence):
        if i == 0:
            if cyclic:
                # use the last element as the predecessor of the first:
                prev = sequence[len(sequence) - 1]
            else:
                prev = elt
                continue
        tuples.append((prev, elt))
        prev = elt
    return tuples


def gen_mask(pointlist, masklength):
    """Generates a binary mask given by a list of indices.

    Takes a list of indices and a length parameter, generates a mask with
    that given length, masking the indices in the given list.
    """
    mask = [0] * masklength
    for point in pointlist:
        mask[point] = 1
    return mask


def vappend(lst, val, desc="list"):
    """Append to a list and log a message according to the loglevel.

    Note: this works only as lists are mutable and we're operating on the
    given list directly.
    """
    log.debug("appending to %s: %s" % (desc, str(val)))
    lst.append(val)


def tesselate(pl1, pl2, dist):
    """Calculates a polygonal partition of a surface in space.

    Takes a distance matrix and two lists of indices (describing sequences
    of points, e.g. filament-like structures) that can be thought of the
    border or rim of an object in space. The two index-lists are required to
    have the same start and end point. The function calculates a partition
    of this object into triangles (tesselation), trying to minimize the
    overall area of all triangles.

    Args:
        pl1, pl2: pointlists (ids of points)
        dist: euclidean distance matrix

    Returns:
        edges: list of tuples with index numbers denoting the edges
    """

    # remove first and last items and get copies of the remaining pointlists
    (start_A, end_A, list_A) = cut_extrema(pl1)
    (start_B, end_B, list_B) = cut_extrema(pl2)
    if start_A != start_B or end_A != end_B:
        raise Exception('Pointlist mismatch.')

    # initialize lists
    edges = []
    triangles = []
    vertices = []
    vappend(edges, (list_A[0], list_B[0]), 'edges')
    vappend(triangles, (list_A[0], list_B[0], start_A), 'triangles')
    vappend(vertices, start_A, 'vertices')

    # Process pointlists A and B simultaneously and determine the distances of
    # A0-B1 and B0-A1. Remove the first element from the list where the
    # shorter edge ends (B0 in case of A0-B1 etc.) and then add the edge A0-B0
    # to the edgelist. If one list reaches its last element, always pop the
    # first element of the other one until both lists have length 1.
    while len(list_A) > 1 or len(list_B) > 1:
        log.debug("-------------\nlist_A: %s\nlist_B: %s" % (list_A, list_B))
        if len(list_A) == 1:
            out = list_B.pop(0)
        elif len(list_B) == 1:
            out = list_A.pop(0)
        else:
            # check distances of A0-B1 and B0-A1
            if dist[list_A[0], list_B[1]] > dist[list_B[0], list_A[1]]:
                out = list_A.pop(0)
            else:
                out = list_B.pop(0)
        vappend(edges, (list_A[0], list_B[0]), 'edges')
        vappend(triangles, (list_A[0], list_B[0], out), 'triangles')
        vappend(vertices, out, 'vertices')
        log.debug("removed 1st element from list: %s" % out)

    # finally add the last triangle containing the endpoint
    vappend(triangles, (list_A[0], list_B[0], end_A), 'triangles')
    vappend(vertices, list_A[0], 'vertices')
    vappend(vertices, list_B[0], 'vertices')
    vappend(vertices, end_A, 'vertices')

    log.info("edges from tesselation: %s" % edges)
    log.debug("triangles from tesselation: %s" % triangles)
    return (edges, triangles, vertices)


def tri_area(p1, p2, p3):
    """Calculate the area of a triangle given by coordinates.

    Uses the property of the cross product of two vectors resulting in
    a vector that (euclidean) norm equals the area of the parallelogram
    defined by the two vectors (and so is double the triangle area)
    """
    v1 = p2 - p1
    v2 = p2 - p3
    return 0.5 * linalg.norm(cross(v1, v2))


def angle(v1u, v2u, normalize=False):
    """Calculate the angle between vectors (in arc degrees).
    .
    Calculates the angle in degrees between two n-dimensional unit vectors
    given as np.ndarrays. The normalization can be done by the function if
    desired. Note that when calculating angles between large number of vectors,
    it is most likely more efficient to normalize them in advance.
    .
    Parameters
    ----------
    v1u, v2u : np.ndarray
        The vectors to compare.
    normalize : bool
        Defines whether we should normalize the given vectors. Otherwise they
        need to be normalized already.
    .
    Returns
    -------
    rad : float
        The angle between the vectors in arc degrees.
    .
    Example
    -------
    >>> import numpy as np
    >>> x = np.array([[1,0,0],[1,0,1]])
    >>> angle(x[0], x[1], normalize=True)
    45.000000000000007
    >>> x = np.array([[1,2,3],[1,2,1]])
    >>> angle(x[0], x[1], normalize=True)
    29.205932247399399
    """
    log.debug('vector shapes: %s %s' % (v1u.shape, v2u.shape))
    if v1u.all() == 0:
        return 0.
    if v2u.all() == 0:
        return 0.
    if normalize:
        v1u = v1u / np.linalg.norm(v1u)
        v2u = v2u / np.linalg.norm(v2u)
    rad = np.arccos(np.dot(v1u, v2u))
    if math.isnan(rad):
        if (v1u == v2u).all():
            rad = 0.0
        else:
            rad = np.pi
    return rad * (180 / np.pi)


def angle2D(v1, v2):
    """Calculate the relative angle between vectors in 2D.
    .
    Calculates the relative angle in degrees between two 2-dimensional vectors
    given as np.ndarrays. Positive numbers correspond to a "right turn", while
    negative numbers correspond to a "left turn".
    .
    Parameters
    ----------
    v1, v2 : np.ndarray
        The vectors to compare.
    .
    Returns
    -------
    rad : float
        The angle between the vectors in arc degrees [-180, 180].
    .
    Example
    -------
    >>> import numpy as np
    >>> x = np.array([[1,1],[1,-11]])
    >>> angle2D(x[0], x[1])
    45.0
    >>> x = np.array([[-3,-0.1],[1.,6.]])
    >>> angle2D(x[0], x[1])
    101.371474641
    """
    if (v1.shape != (2,) or v2.shape != (2,)):
        raise TypeError('Can handle only 2-D vectors!')
    x_coords = np.array([v1[0], v2[0]])
    y_coords = np.array([v1[1], v2[1]])
    # arctan2() gives the angles between (1,0) and the vector defined by the
    # coordinates, and it takes Y coords first, then X...
    angles = np.arctan2(y_coords, x_coords)
    log.debug(math.degrees(angles[0]))
    log.debug(math.degrees(angles[1]))
    delta = math.degrees(angles[1] - angles[0])
    # we need to compensate a possible "overflow" manually:
    if (abs(delta) > 180):
        delta = 360 - abs(delta)
    return delta
