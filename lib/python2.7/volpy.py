#!/usr/bin/python

"""Discrete volumetric data tools.

Provides distance, area, mesh-related calculations on spots
in three dimensional space.
"""

from log import log
import numpy as np
import numpy.matlib as matlib
import scipy
import math
import pprint
import csv
from aux import filename

# TODO:
# - make a real package from this and split into submodules
# - extend the Filament class to be able to return the masks of the individual
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
    'Filament',
    'Points3D',
    'GreedyPath',
    'CellJunction',
    # 'find_neighbor',
    # 'gen_mask',
    # 'gen_unmask',
]

ppr = pprint.PrettyPrinter(indent=4)

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


def get_max_dist_pair(matrix):
    """Determine points with largest distance using a distance matrix.

    Args:
        matrix: euclidean distance matrix

    Returns:
        (i1, i2): tuple of index numbers of the largest distance pair.
    """
    # TODO: this can be done with argmax()
    maxdist = 0
    pair = (-1, -1)
    for row_num, row in enumerate(matrix):
        row_max = max(row)
        if row_max > maxdist:
            maxdist = row_max
            max_pos = matlib.where(row == row_max)[0][0]
            pair = (row_num, max_pos)
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
    masked_dists = np.ma.array(dist_mat[pid], mask=mask)
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


def gen_mask(pointlist, masklength):
    """Generates a binary mask given by a list of indices.

    Takes a list of indices and a length parameter, generates a mask with
    that given length, masking the indices in the given list.

    Parameters
    ----------
    pointlist : list(int)
        The list of indices that should be masked.
    masklength : int
        The length of the mask to produce.

    Returns
    -------
    mask : list([0,1])
        The mask with the desired indices masked.

    Example
    -------
    >>> gen_mask([1,3,4,7,8], 11)
    [0, 1, 0, 1, 1, 0, 0, 1, 1, 0, 0]
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
    (start_a, end_a, list_a) = cut_extrema(pl1)
    (start_b, end_b, list_b) = cut_extrema(pl2)
    if start_a != start_b or end_a != end_b:
        raise Exception('Pointlist mismatch.')

    # initialize lists
    edges = []
    triangles = []
    vertices = []
    try:
        vappend(edges, (list_a[0], list_b[0]), 'edges')
    except IndexError as err:
        raise SystemExit("%s: list_a = %s -- list_b = %s" % \
            (err, list_a, list_b))

    vappend(triangles, (list_a[0], list_b[0], start_a), 'triangles')
    vappend(vertices, start_a, 'vertices')

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
            if dist[list_a[0], list_b[1]] > dist[list_b[0], list_a[1]]:
                out = list_a.pop(0)
            else:
                out = list_b.pop(0)
        vappend(edges, (list_a[0], list_b[0]), 'edges')
        vappend(triangles, (list_a[0], list_b[0], out), 'triangles')
        vappend(vertices, out, 'vertices')
        log.debug("removed 1st element from list: %s" % out)

    # finally add the last triangle containing the endpoint
    vappend(triangles, (list_a[0], list_b[0], end_a), 'triangles')
    vappend(vertices, list_a[0], 'vertices')
    vappend(vertices, list_b[0], 'vertices')
    vappend(vertices, end_a, 'vertices')

    log.info("edges from tesselation: %s" % edges)
    log.debug("triangles from tesselation: %s" % triangles)
    return (edges, triangles, vertices)


def tri_area(point1, point2, point3):
    """Calculate the area of a triangle given by coordinates.

    Uses the property of the cross product of two vectors resulting in
    a vector that (euclidean) norm equals the area of the parallelogram
    defined by the two vectors (and so is double the triangle area)

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
    >>> import numpy as np
    >>> tri_area(np.array([3,0,0]), np.array([0,4,0]), np.array([0,0,0]))
    6.0
    >>> tri_area(np.array([95.6, 66.8, 17.8]), np.array([83.8, 75.3, 28.9]),
    ...     np.array([75.6, 46.1, 13.4]))
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
        (self.edges, self.triangles, self.vertices) = \
            tesselate(self._fil2.path, self._fil1.path, self.get_edm())
        log.warn("------------ largest distance results -------------")
        log.warn("idx numbers:\t" + ppr.pformat(self.get_mdpair()))
        log.warn("coordinates:\t" + ppr.pformat(self.get_mdpair_coords()))
        log.warn("distance:\t" + ppr.pformat(self.get_mdpair_dist()))
        log.warn("---------------------------------------------------")
        log.warn("perimeter: %s" % self.perimeter)
        log.debug("vertices: %s" % self.vertices)
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


### TODO: the matplotlib stuff should go into a submodule!
import matplotlib.pyplot as plt
from matplotlib.colors import colorConverter
# http://matplotlib.org/api/colors_api.html

# stuff required for matplotlib:
from mpl_toolkits.mplot3d import Axes3D
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
import numpy as np


def plot3d_scatter(plot, points, color, linewidth=1):
    """Do a 3D scatter plot with the given points."""
    # x, y, z are fine in this context, so disable this pylint message here:
    # pylint: disable-msg=C0103
    # we need to have the coordinates as 3 ndarrays (x,y,z):
    x, y, z = np.asarray(zip(points[0], points[1]))
    plot.scatter(x, y, z, zdir='z', c=color, linewidth=linewidth)


def plot3d_line(plot, points, color, linewidth=1):
    """Plot a line in 3D from the given points."""
    # x, y, z are fine in this context, so disable this pylint message here:
    # pylint: disable-msg=C0103
    # we need to have the coordinates as 3 ndarrays (x,y,z):
    x, y, z = np.asarray(zip(points[0], points[1]))
    plot.plot(x, y, z, zdir='z', c=color, linewidth=linewidth)


def plot3d_maxdist(axes, maxdist_points):
    """Plot and label the points with maximum distance.

    Parameters
    ----------
    axes : mpl_toolkits.mplot3d.Axes3D
    maxdist_points : tuple of np.ndarray (shape = (3,))

    Returns
    -------
    (pos, dist)
    pos : np.array
    dist : float

    Example
    -------
    >>> fig = plt.figure()
    >>> axes = Axes3D(fig)
    >>> point1 = np.array([76.123, 77.062, -7.5684])
    >>> point2 = np.array([98.758, 36.733, 5.4777])
    >>> plot3d_maxdist(axes, (point1, point2))
    (array([ 87.4405 ,  56.8975 ,  -1.04535]), 48.051765744975484)
    """
    plot3d_scatter(axes, maxdist_points, 'r', linewidth=18)
    for i in (0, 1):
        axes.text(*maxdist_points[i], color='blue',
            s='   (%s | %s | %s)' % (maxdist_points[i][0],
            maxdist_points[i][1], maxdist_points[i][2]))
    # draw connection line between points:
    plot3d_line(axes, maxdist_points, 'y')
    # calculate length and add label:
    pos = maxdist_points[1] + ((maxdist_points[0] - maxdist_points[1]) / 2)
    dist = np.linalg.norm(maxdist_points[0] - maxdist_points[1])
    axes.text(pos[0], pos[1], pos[2], color='blue', s='%.2f' % dist)
    return (pos, dist)


def plot3d_label_axes(axes, labels):
    """Label the axes of a 3D plot."""
    axes.set_xlabel(labels[0])
    axes.set_ylabel(labels[1])
    axes.set_zlabel(labels[2])


def plot3d_set_minmax(axes, points3d_object):
    """Determine min and max coordinates and set limits.

    Parameters
    ----------
    axes : mpl_toolkits.mplot3d.Axes3D
    points3d_object : Points3D

    Returns
    -------
    (cmin, cmax)
    cmin, cmax : np.array (shape = (3,))
    """
    data = points3d_object.get_coords()
    cmin = data.min(axis=0)
    cmax = data.max(axis=0)
    axes.set_xlim3d(cmin[0], cmax[0])
    axes.set_ylim3d(cmin[1], cmax[1])
    axes.set_zlim3d(cmin[2], cmax[2])
    return cmin, cmax


def plot3d_filaments(axes, points3d_object):
    """Draw edges along a filament pointlist."""
    data = points3d_object.get_coords()
    adjacent = sort_neighbors(points3d_object.get_edm())
    log.debug(adjacent)
    for pair in build_tuple_seq(adjacent, cyclic=True):
        coords = [data[pair[0]], data[pair[1]]]
        plot3d_line(axes, coords, 'm')


def plot3d_tess_edges(axes, points3d_object):
    """Draw edges from tesselation results."""
    data = points3d_object.get_coords()
    colors = ['r', 'g', 'b', 'y', 'c', 'm']
    for i, pair in enumerate(points3d_object.edges):
        coords = [data[pair[0]], data[pair[1]]]
        curcol = colors[i % 6]
        plot3d_line(axes, coords, curcol)


def plot3d_tess_tri(axes, points3d_object):
    """Draw triangle areas from tesselation results."""
    rgb = lambda arg: colorConverter.to_rgba(arg, alpha=0.6)
    colors = ['r', 'g', 'b', 'y', 'c', 'm']
    for i, vtx in enumerate(points3d_object.get_vertices()):
        curcol = colors[i % 6]
        tri = Poly3DCollection([vtx], facecolors=rgb(curcol), linewidth=0)
        tri.set_alpha(0.8)
        axes.add_collection3d(tri)


def plot3d_junction(points3d_object, show, export):
    """Create a 3D plot of a junction object."""

    # prepare the figure
    fig = plt.figure()
    axes = Axes3D(fig)

    plot3d_set_minmax(axes, points3d_object)
    plot3d_label_axes(axes, ('X', 'Y', 'Z'))

    # # print overall area and maximum tesselation edge length:
    # axes.text(*cmin, s='  overall area: %.2f' % points3d_object.get_area(),
    #     color='blue')
    # axes.text(*points3d_object.get_longest_edge_pos(), color='blue',
    #     s='  longest edge: %.2f' % points3d_object.get_longest_edge())

    # draw the raw filament points:
    # TODO: add commandline switch to enable this!
    # plot3d_scatter(axes, data, 'w')

    plot3d_maxdist(axes, points3d_object.get_mdpair_coords())
    plot3d_filaments(axes, points3d_object)
    plot3d_tess_edges(axes, points3d_object)
    plot3d_tess_tri(axes, points3d_object)

    if export:
        plot3d_pngseries(export, axes)
    if show:
        plot3d_show()


def plot3d_pngseries(outdir, axes):
    """Export a 3D plot as a series of PNGs, rotating in 1 deg steps.

    Parameters
    ----------
    outdir : str
        The path of an existing directory to store the PNGs in.
    axes : Axes3D object
        The axes object of the plot.
    """
    log.warn("exporting 3D plot to PNG files...")
    for azimuth in range(360):
        # we start at 60 deg, it just looks nicer:
        axes.azim = azimuth + 60
        fname = '%s/3dplot-%03d.png' % (outdir, azimuth)
        log.info("saving plot %i as '%s'" % (azimuth, fname))
        plt.savefig(fname)
    log.warn("done")


def plot3d_show():
    """Show an interactive 3D plot of the data."""
    # disabling the blocking mode makes the script return immediately
    # without showing anything, unless a couple of draw() statements
    # follow
    plt.show()
    # to show an animation the following code could be used:
    # plt.show(block=False)
    # for azim in range(60, 420):
    #     axes.azim = azim
    #     plt.draw()
    #     # to add a delay, the time module must be imported:
    #     # time.sleep(0.025)


if __name__ == "__main__":
    print('Running doctest on this module...')
    import doctest
    doctest.testmod()
