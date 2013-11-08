#!/usr/bin/python

"""Discrete volumetric data tools.

Provides distance, area, mesh-related calculations on spots in three
dimensional space.
"""

from log import log
import numpy as np
import numpy.matlib as matlib
import scipy
import math
import pprint
import csv
from misc import filename

# TODO:
# - extend the Filament class to be able to return the masks of the individual
#   filaments, access to start and end points, etc.
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
    'Filament',
    'Points3D',
    'GreedyPath',
    'CellJunction',
    # 'find_neighbor',
    # 'make_mask_by_index',
    # 'gen_unmask',
]

ppr = pprint.PrettyPrinter(indent=4)


def dist_matrix(pts):
    """Calculate the euclidean distance matrix (EDM) for a set of points.

    Parameters
    ----------
    pts : np.ndarray (shape = (2,))

    Returns
    -------
    dist_mat : np.ndarray
        The distance matrix as 2d ndarray.

    Implementation Details
    ----------------------
    Uses two auxiliary matrixes to easily calculate the distance from each
    point to every other point in the list using this approach:
    (1) aux matrixes:
    repmat(l, n1, n2): l is repeated n1 times, along axis 1, and n2 times along
    axis 2, so repmat(pts, len(pts), 1) =
        array( [ [1, 2], [4, 6], [1, 2], [4, 6] ] )
    repeat(l, n, a): each element of l is repeated n times along axis a (w/o
    'a' a plain list is generated), so repeat(pts, 2, 1) =
        array( [ [1, 2], [1, 2], [4, 6], [4, 6] ] )
    (2) Pythagoras:
    Then, the element-wise difference of the generated matrixes is calculated
    each value is squared:
        array( [ [ 0,  0], [ 9, 16], [ 9, 16], [ 0,  0] ] )
    These squares are then summed up (linewise) using sum(..., axis=1):
        array([ 0, 25, 25,  0])
    Finally the square root is taken for each element:
        array([ 0.,  5.,  5.,  0.])
    To transform the list into a distance matrix reshape() is used.

    Example
    -------
    >>> dist_matrix([ [1, 2], [4, 6] ])
    array([[ 0.,  5.],
           [ 5.,  0.]])
    >>> dist_matrix([ [1.8, 4.1, 4.0], [2.8, 4.7, 4.5], [5.2, 4.2, 4.7],
    ...               [4.1, 4.5, 4.6], [5.7, 3.4, 4.5]])
    array([[ 0.        ,  1.26885775,  3.47275107,  2.41039416,  3.99374511],
           [ 1.26885775,  0.        ,  2.45967478,  1.3190906 ,  3.17804972],
           [ 3.47275107,  2.45967478,  0.        ,  1.14455231,  0.96436508],
           [ 2.41039416,  1.3190906 ,  1.14455231,  0.        ,  1.94422221],
           [ 3.99374511,  3.17804972,  0.96436508,  1.94422221,  0.        ]])
    """
    dist_mat = scipy.sqrt(
        matlib.sum(
            (
                matlib.repmat(pts, len(pts), 1) -
                matlib.repeat(pts, len(pts), axis=0)
            ) ** 2,
                           axis=1
        )
    )
    return dist_mat.reshape((len(pts), len(pts)))


def get_max_dist_pair(edm):
    """Determine points with largest distance using a distance matrix.

    Parameters
    ----------
    edm : euclidean distance matrix

    Returns
    -------
    (i1, i2) : tuple(int)
        The tuple of index numbers of the largest distance pair.

    Example
    -------
    >>> edm = dist_matrix([ [1.8, 4.1, 4.0], [2.8, 4.7, 4.5], [5.2, 4.2, 4.7],
    ...                     [4.1, 4.5, 4.6], [3.7, 3.4, 4.5]])
    >>> get_max_dist_pair(edm)
    (0, 2)
    """
    # argmax() does the main job of finding the largest entry, unravel_index()
    # converts the index back to the tuple usable for the 2d edm array
    return np.unravel_index(edm.argmax(), edm.shape)


def get_min_dist_pair(edm, split):
    """Get points with minimal distance from set_1 to set_2.

    Take an EDM and an index number splitting the EDM into two parts ("set_1"
    and "set_2") and identify the tuple (point_1, point_2) with the minimal
    distance where "point_N" is from "set_N".

    Parameters
    ----------
    edm : euclidean distance matrix
    split : int
        The index number where to split the EDM.

    Returns
    -------
    (i1, i2) : tuple(int)
        The tuple of index numbers of the minimal distance pair. If more than
        one pair has the same minimal distance, the first one (in row-col
        order) is returned.

    Example
    -------
    2 |     *   *
    1 | x     *   x
    0-+------------
      0 1 2 3 4 5 6
    >>> pl1 = np.array([[1,1],[6,1]])  # marked as 'x' above
    >>> pl2 = np.array([[3,2],[4,1],[5,2]])  # marked as '*' above
    >>> edm =  dist_matrix(np.vstack([pl1, pl2]))
    >>> get_min_dist_pair(edm, 2)
    (1, 4)
    """
    subset = edm[:split, split:]
    # argmin() returns the smallest entry, unravel_index() converts the index
    # back to the tuple usable for the 2d edm array
    minpos = np.unravel_index(subset.argmin(), subset.shape)
    log.debug(subset)
    log.info(minpos)
    log.info(subset[minpos])
    log.info('---')
    # now we need to convert the array coordinates back to the form usable
    # with the original (non-subset) EDM:
    minpos_orig = (minpos[0], minpos[1] + split)
    log.debug(edm)
    log.info(minpos_orig)
    log.info(edm[minpos_orig])
    return minpos_orig


def find_neighbor(pid, edm, mask):
    """Find the closest neighbor in a given distance matrix.

    Take a reference point and look up the closest neighbor in a masked
    distance matrix. The mask can be used to exclude selected points in the
    calculation, for example when they have already been processed earlier.
    Otherwise use a 0-mask.

    Parameters
    ----------
    pid : int
        The index of the reference point.
    edm : EDM
        The euclidean distance matrix of all points.
    mask : list
        The binary list to use as a mask.

    Returns
    -------
    closest : int
        The index of the closest neighbor.

    Example
    -------
    >>> edm = dist_matrix([ [1.8, 4.1, 4.0], [2.8, 4.7, 4.5], [5.2, 4.2, 4.7],
    ...                     [4.1, 4.5, 4.6], [3.7, 3.4, 4.5]])
    >>> find_neighbor(3, edm, 0)
    2
    >>> find_neighbor(2, edm, [0,0,1,1,0])
    4
    """
    # we need to make sure at least the reference point is masked, so first
    # make sure the mask is a full array, then mask our reference id
    if mask == 0:
        mask = np.zeros(edm.shape[0])
    mask[pid] = 1
    return np.ma.array(edm[pid], mask=mask).argmin()


def path_greedy(edm, mask_ref, pair):
    """Use greedy search to find a path between a pair of points.

    Take a euclidean distance matrix, a mask and a tuple denoting the start and
    stop index, calculate a path from first to last using the greedy approach
    by always taking the closest element next that has not yet been processed.
    Processed points will be disabled in the mask.

    Parameters
    ----------
        edm : EDM
            The euclidean distance matrix of all points.
        mask_ref : list
            The array mask (a binary list) or 'None'.
        pair : tuple(int)
            The pair of index numbers denoting start and stop.

    Returns
    -------
    (sequence, mask, pathlen)
        sequence : list
            The list of indices denoting the greedy path.
        mask : list
            The mask of the above sequence.
        pathlen : int
            The overall length of the path.

    Example
    -------
    >>> edm = dist_matrix([ [1.8, 4.1, 4.0], [2.8, 4.7, 4.5], [5.2, 4.2, 4.7],
    ...                     [4.1, 4.5, 4.6], [3.7, 3.4, 4.5]])
    >>> path_greedy(edm, [0,0,1,0,0], (3,0))
    ([3, 4, 1, 0], [1, 1, 1, 1, 1], 4.024730596576215)
    """
    sequence = []
    pathlen = 0

    if mask_ref is None:
        # create an empty mask with the number of points:
        mask = [0] * len(edm[0])
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
        closest = find_neighbor(cur, edm, mask)
        pathlen += edm[cur, closest]
        log.debug('accumulated path length: %s' % pathlen)
        if closest == pair[1]:
            sequence.append(pair[1])
            mask[closest] = 1
            break
        cur = closest
    log.info('path length: %s' % pathlen)
    log.info('path (%s->%s): %s' % (pair[0], pair[1], sequence))
    return (sequence, mask, pathlen)


def cut_extrema(lst):
    """Return the first & last element and the rest of a list (copied).

    Example
    -------
    >>> cut_extrema([1, 2, 3, 4, 5, 6, 7, 8, 9])
    (1, 9, [2, 3, 4, 5, 6, 7, 8])
    """
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


def sort_neighbors(edm):
    """Sort a list of indices to minimize the distance between elements.

    Take an EDM and iteratively build a list of indices where each point is
    followed by its closest neighbor, starting at point 0 of the distance
    matrix.

    Parameters
    ----------
    edm : EDM
        The euclidean distance matrix of all points.

    Returns
    -------
    adjacents : list
        The list of indices in sorted order.

    Example
    -------
    >>> edm = dist_matrix([ [1.8, 4.1, 4.0], [2.8, 4.7, 4.5], [5.2, 4.2, 4.7],
    ...                     [4.1, 4.5, 4.6], [3.7, 3.4, 4.5]])
    >>> sort_neighbors(edm)
    [0, 1, 3, 2, 4]
    """
    adjacents = []

    # inital mask is 0 everywhere (no masking at all):
    mask = [0] * edm.shape[0]

    # for convenience we use a set instead of a list, so we don't have
    # to care on what position the current element is
    pointset = set(range(edm.shape[0]))
    cur = 0
    while len(pointset) > 0:
        adjacents.append(cur)
        pointset.remove(cur)
        mask[cur] = 1
        closest = find_neighbor(cur, edm, mask)
        # print str(cur) + ' - ' + str(closest)
        cur = closest
    log.debug(adjacents)
    return adjacents


def build_tuple_seq(sequence, cyclic=False):
    """Convert a sequence into a list of 2-tuples.

    Take a sequence (list) and return a list of 2-tuples where each tuple
    consists of the previous list entry and the current one, starting with the
    entry (last, 1st), then (1st, 2nd) and so on.

    The optional parameter "cyclic" states whether the sequnce should by cyclic
    or acyclic, meaning the last and the first element will be connected or
    not.

    Parameters
    ----------
    sequence : list
        A sequence of index numbers.
    cyclic : bool

    Returns
    -------
    tuples : list of tuples

    Example
    -------
    >>> build_tuple_seq([1,3,4,7,8])
    [(1, 3), (3, 4), (4, 7), (7, 8)]
    >>> build_tuple_seq([1,3,4,7,8], cyclic=True)
    [(8, 1), (1, 3), (3, 4), (4, 7), (7, 8)]
    """
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


def make_mask_by_index(pointlist, masklength):
    """Generate a mask from a list of index numbers.

    Take a list of indices and a length parameter, generate a mask with that
    given length, masking the indices in the given list.

    Parameters
    ----------
    pointlist : list(int)
        The list of indices that should be masked.
    masklength : int
        The length of the mask to produce.

    Returns
    -------
    mask : ndarray(dtype=bool)
        A boolean mask with the desired indices masked.

    Example
    -------
    >>> make_mask_by_index([1,3,4,7,8], 11)
    array([False,  True, False,  True,  True, False, False,  True,  True,
           False, False], dtype=bool)
    """
    mask = np.ma.make_mask_none((masklength,))
    for point in pointlist:
        mask[point] = True
    return mask


def vappend(lst, val, desc="list"):
    """Append to a list and log a message according to the loglevel.

    Note: this works only as lists are mutable and we're operating on the
    given list directly.
    """
    log.debug("appending to %s: %s" % (desc, str(val)))
    lst.append(val)


def tesselate(pl1, pl2, edm):
    """Calculate a polygonal partition of a surface in space.

    Take a distance matrix and two lists of indices (describing sequences of
    points, e.g. filament-like structures) that can be thought of the border or
    rim of an object in space. The two index-lists are required to have the
    same start and end point. The function calculates a partition of this
    object into triangles (tesselation), trying to minimize the overall area of
    all triangles.

    If one or both pointlists have less than 3 entries, an IndexError will be
    raised - this case is simply not covered yet, as no real-world application
    produced such data.

    Parameters
    ----------
    pl1, pl2 : lists
        The pointlists (index numbers).
    edm : EDM
        The euclidean distance matrix.

    Returns
    -------
    (edges, triangles)
    edges : list(tuple)
        The list of pairs of index numbers denoting the edges.
    triangles : list(triplets)
        The list of 3-tuples denoting the vertices of the triangles.

    Example
    -------
    >>> edm = dist_matrix([ [0,4], [4,2], [7,3], [8,6], [5,8], [3,5] ])
    >>> pl1 = [0, 1, 2, 3]
    >>> pl2 = [0, 5, 4, 3]
    >>> (edges, triangles) = tesselate(pl1, pl2, edm)
    >>> print(edges)
    [(1, 5), (2, 5), (2, 4)]
    >>> print(triangles)
    [(1, 5, 0), (2, 5, 1), (2, 4, 5), (2, 4, 3)]

    >>> tesselate([0,1,2,5], pl2, edm)
    Traceback (most recent call last):
      (Traceback stack omitted)
    IndexError: Pointlist mismatch.
    >>> tesselate([0,3], pl2, edm)
    Traceback (most recent call last):
      (Traceback stack omitted)
    IndexError: Pointlist too short.
    """
    # remove first and last items and get copies of the remaining pointlists
    (start_a, end_a, list_a) = cut_extrema(pl1)
    (start_b, end_b, list_b) = cut_extrema(pl2)
    if start_a != start_b or end_a != end_b:
        raise IndexError('Pointlist mismatch.')
    if len(list_a) == 0 or len(list_b) == 0:
        raise IndexError('Pointlist too short.')

    edges = []
    triangles = []
    vappend(edges, (list_a[0], list_b[0]), 'edges')
    vappend(triangles, (list_a[0], list_b[0], start_a), 'triangles')

    # Process pointlists A and B simultaneously and determine the distances of
    # A0-B1 and B0-A1. Remove the first element from the list where the
    # shorter edge ends (B0 in case of A0-B1 etc.) and then add the edge A0-B0
    # to the edgelist. If one list reaches its last element, always pop the
    # first element of the other one until both lists have length 1.
    while len(list_a) > 1 or len(list_b) > 1:
        log.debug("-------------\nlist_A: %s\nlist_B: %s" % (list_a, list_b))
        if len(list_a) == 1:
            out = list_b.pop(0)
        elif len(list_b) == 1:
            out = list_a.pop(0)
        else:
            # check distances of A0-B1 and B0-A1
            if edm[list_a[0], list_b[1]] > edm[list_b[0], list_a[1]]:
                out = list_a.pop(0)
            else:
                out = list_b.pop(0)
        vappend(edges, (list_a[0], list_b[0]), 'edges')
        vappend(triangles, (list_a[0], list_b[0], out), 'triangles')
        log.debug("removed 1st element from list: %s" % out)
    # finally add the last triangle containing the endpoint
    vappend(triangles, (list_a[0], list_b[0], end_a), 'triangles')

    log.info("edges from tesselation: %s" % edges)
    log.debug("triangles from tesselation: %s" % triangles)
    return (edges, triangles)


def tri_area(point1, point2, point3):
    """Calculate the area of a triangle given by coordinates.

    Uses the property of the cross product of two vectors resulting in a vector
    that (euclidean) norm equals the area of the parallelogram defined by the
    two vectors (and so is double the triangle area)

    Parameters
    ----------
    point1, point2, point3 : np.array
        The vectors of the triangle's vertices.

    Returns
    -------
    area : float
        The area of the triangle in square units.

    Example
    -------
    >>> from numpy import array
    >>> tri_area(array([3,0,0]), array([0,4,0]), array([0,0,0]))
    6.0
    >>> tri_area(array([95.6, 66.8, 17.8]), array([83.8, 75.3, 28.9]),
    ...     array([75.6, 46.1, 13.4]))
    266.29388412992131
    """
    vec1 = point2 - point1
    vec2 = point2 - point3
    return 0.5 * np.linalg.norm(np.cross(vec1, vec2))


def angle(v1u, v2u, normalize=False):
    """Calculate the angle between vectors (in arc degrees).

    Calculates the angle in degrees between two n-dimensional unit vectors
    given as np.ndarrays. The normalization can be done by the function if
    desired. Note that when calculating angles between large number of vectors,
    it is most likely more efficient to normalize them in advance.

    Parameters
    ----------
    v1u, v2u : np.ndarray
        The vectors to compare.
    normalize : bool
        Defines whether we should normalize the given vectors. Otherwise they
        need to be normalized already.

    Returns
    -------
    rad : float
        The angle between the vectors in arc degrees.

    Example
    -------
    >>> import numpy as np
    >>> x = np.array([[1,0,0], [1,0,1]])
    >>> angle(x[0], x[1], normalize=True)
    45.000000000000007
    >>> x = np.array([[1,2,3], [1,2,1]])
    >>> angle(x[0], x[1], normalize=True)
    29.205932247399399
    >>> x = np.array([[0,0,0], [1,2,1]])
    >>> angle(x[0], x[1], normalize=True)
    0.0
    >>> x = np.array([[1,2,1], [0,0,0]])
    >>> angle(x[0], x[1], normalize=True)
    0.0
    """
    log.debug('vector shapes: %s %s' % (v1u.shape, v2u.shape))
    if not v1u.any():
        return 0.
    if not v2u.any():
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


def angle_2d(vec1, vec2):
    """Calculate the relative angle between vectors in 2D.

    Calculates the relative angle in degrees between two 2-dimensional vectors
    given as np.ndarrays. Positive numbers correspond to a "right turn", while
    negative numbers correspond to a "left turn".

    Parameters
    ----------
    vec1, vec2 : np.ndarray
        The vectors to compare.

    Returns
    -------
    rad : float
        The angle between the vectors in arc degrees [-180, 180].

    Example
    -------
    >>> import numpy as np
    >>> angle_2d(np.array([1,0]), np.array([1,0]))
    0.0
    >>> angle_2d(np.array([1,0]), np.array([0,1]))
    90.0
    >>> angle_2d(np.array([1,1]), np.array([1,-1]))
    -90.0
    >>> angle_2d(np.array([3,0.6]), np.array([-3,-0.0]))
    168.69006752597977
    >>> angle_2d(np.array([-3,-0.1]), np.array([1,6]))
    -101.37147464102202
    >>> angle_2d(np.array([1,0]), np.array([-1,0]))
    180.0
    """
    if (vec1.shape != (2,) or vec2.shape != (2,)):
        raise TypeError('Can handle only 2-D vectors!')
    x_coords = np.array([vec1[0], vec2[0]])
    y_coords = np.array([vec1[1], vec2[1]])
    # arctan2() gives the angles between (1,0) and the vector defined by the
    # coordinates, and it takes Y coords first, then X...
    angles = np.arctan2(y_coords, x_coords)
    delta = math.degrees(angles[1] - angles[0])
    # we need to compensate a possible "overflow" manually:
    if delta < -180:
        log.debug('delta below -180')
        delta = 360 - abs(delta)
    if delta > 180:
        log.debug('delta above 180')
        delta = -360 + abs(delta)
    log.debug('angle_2d(%s, %s): %f' % (vec1, vec2, delta))
    return delta


class Points3D(object):

    """Class for points in 3D space given their coordinates."""

    def __init__(self, csvfile):
        """Load point coordinates from a CSV file."""
        self.edm = None
        self.mdpair = None
        # np.loadtxt() returns an ndarray() of floats, complains on non-floats
        self.data = np.loadtxt(csvfile, delimiter=',')
        log.info('Parsed %i points from CSV.\n%s' %
            (len(self.data), str(self.data)))
        log.debug(ppr.pformat(self.data))

    def get_coords(self):
        """Get the coordinates of this object as np.ndarray."""
        return self.data

    def get_edm(self):
        """Get the euclidean distance matrix of the points."""
        # lazy initialization of the EDM:
        if self.edm == None:
            self.edm = dist_matrix(self.data)
            log.info(ppr.pformat(self.edm))
        return self.edm

    def get_mdpair(self):
        """Get the pair of points with the maximum distance.

        Returns
        -------
        mdpair : (int, int)
          The tuple of index numbers for the described points.
        """
        # lazy initialization of the maxdistpair:
        if self.mdpair == None:
            self.mdpair = get_max_dist_pair(self.get_edm())
        return self.mdpair

    def get_mdpair_coords(self):
        """Get the coordinates of the maximum distance pair.

        Returns
        -------
        mdpair_coords : (ndarray, ndarray)
          The tuple of coordinates for the described points.
        """
        # NOTE: previously this was a list, not a tuple...
        return (self.data[self.get_mdpair()[0]],
            self.data[self.get_mdpair()[1]])

    def get_mdpair_dist(self):
        """Get the distance of the maximum distance pair.

        Returns
        -------
        dist : float
        """
        return self.get_edm()[self.get_mdpair()]

    def gen_bitmap(self, size, crop=False, delta=1):
        """Generate a 2D bitmap of the coordinates.

        The bitmap is a matrix (size[0] x size[1]) with all values set to
        zero, except those where an object exists (converted from object
        coordinate space to the bitmap coordinate space).

        Parameters
        ----------
        size : (int, int)
        crop : Bool
            Set to True if empty parts of the target coordinate space should
            be cropped away before generating the bitmap.
        delta : int
            Can be used to specify the offset that gets added at a position
            when an object is mapped to a pixel.

        Returns
        -------
        bitmap : ndarray
        """
        coords = self.data
        xmin = coords[:, 0].min()
        ymin = coords[:, 1].min()
        xmax = coords[:, 0].max()
        ymax = coords[:, 1].max()

        bitmap = np.zeros((size[0], size[1]), dtype=np.int)
        for point in coords:
            pix_x = int((point[0] / xmax) * (size[0] - 1))
            pix_y = int((point[1] / ymax) * (size[1] - 1))
            # print "(%f,%f) -> (%i,%i)" % (point[0], point[1], pix_x, pix_y)
            if crop:
                pix_x -= xmin
                pix_y -= ymin
            bitmap[pix_x, pix_y] += delta

        return bitmap


class Filament(Points3D):
    """Filament objects in 3D space based on a Points3D object."""
    pass


class GreedyPath(object):

    """Construct greedy paths from points in 3D space."""

    def __init__(self, points_3d, extrema, mask):
        """Calculate the greedy path from extrema[0] to extrema[1]."""
        (self.path, self.mask, self.length) = \
            path_greedy(points_3d.get_edm(), mask, extrema)


class CellJunction(Points3D):

    """Class representing cell junctions (rims of touching areas)."""

    def __init__(self, csvfile):
        """Run tesselation method to calculate an area approximation.

        The points with the maximum distance in the given Points3D object are
        considered to be the extrema of the cell junction, they are used to
        build the connecting paths and to run the tesselation algorithm.
        """
        super(CellJunction, self).__init__(csvfile)
        self._te_max = 0   # longest transversal edge
        self._te_max_pos = None   # used to place the label with matplotlib
        self._vtxlist = []   # a list of lists of 3-tuples of coordinates
        self._area = 0   # combined area of all tesselation polygons

        # First calculate the shortest path using *all* points, then calculate
        # the shortest path using only the remaining points. This results in
        # two separate point lists forming a loop that can then be used for the
        # tesselation procedure.
        self._fil1 = GreedyPath(self, self.get_mdpair(), None)
        self._fil2 = GreedyPath(self, self.get_mdpair(), self._fil1.mask)
        self.perimeter = self._fil1.length + self._fil2.length
        (self.edges, self.triangles) = \
            tesselate(self._fil2.path, self._fil1.path, self.get_edm())
        log.warn("------------ largest distance results -------------")
        log.warn("idx numbers:\t" + ppr.pformat(self.get_mdpair()))
        log.warn("coordinates:\t" + ppr.pformat(self.get_mdpair_coords()))
        log.warn("distance:\t" + ppr.pformat(self.get_mdpair_dist()))
        log.warn("---------------------------------------------------")
        log.warn("perimeter: %s" % self.perimeter)
        log.debug("edges: %s" % self.edges)

    def get_longest_edge(self):
        """Determine the longest transversal edge from the tesselation."""
        if self._te_max == 0:
            for edge in self.edges:
                curlen = self.get_edm()[edge[0], edge[1]]
                if curlen > self._te_max:
                    self._te_max = curlen
                    self._te_max_pos = self.data[edge[0]]   # store position
            log.warn("longest edge from tesselation: %s" % self._te_max)
        return self._te_max

    def get_longest_edge_pos(self):
        """Look up the length of the longest transversal edge."""
        if self._te_max_pos == None:
            self.get_longest_edge()
        return self._te_max_pos

    def get_vertices(self):
        """Calculate the list of vertices of the tesselation result."""
        if self._vtxlist == []:
            for (vtx1, vtx2, vtx3) in self.triangles:
                self._vtxlist.append([tuple(self.data[vtx1]),
                    tuple(self.data[vtx2]), tuple(self.data[vtx3])])
                self._area += tri_area(self.data[vtx1],
                    self.data[vtx2], self.data[vtx3])
            log.debug("vtxlist: %s" % self._vtxlist)
        return self._vtxlist

    def get_area(self):
        """Calculate the area of the tesselation result."""
        # The actual calculation is done when creating the list of vertices, so
        # we just check if that was already done or delegate it otherwise.
        if self._area == 0:
            self.get_vertices()
            log.warn("overall area: %s" % self._area)
        return self._area

    def write_output(self, f_out, f_in):
        """Assemble output file with collected results."""
        out = csv.writer(f_out, dialect='excel', delimiter=';')
        write = out.writerow
        mdpair = self.get_mdpair()
        mdpts = self.get_mdpair_coords()
        write(['input filename', filename(f_in)])
        write([])
        write(['distance results'])
        write(['largest distance points (indices)', str(mdpair)])
        write(['coordinates of point %s' % mdpair[0], mdpts[0]])
        write(['coordinates of point %s' % mdpair[1], mdpts[1]])
        write(['distance', str(self.get_edm()[mdpair])])
        write([])
        write(['area results calculated by triangular tesselation'])
        write(['longest transversal edge', self.get_longest_edge()])
        write(['overall area', self.get_area()])
        write(['perimeter', self.perimeter])


if __name__ == "__main__":
    print('Running doctest on file "%s".' % __file__)
    import doctest
    doctest.testmod()
