#!/usr/bin/python

"""Plotting submodule for volpy using matplotlib."""

from log import log
from volpy import sort_neighbors, build_tuple_seq

import matplotlib.pyplot as plt
from matplotlib.colors import colorConverter
# http://matplotlib.org/api/colors_api.html

from mpl_toolkits.mplot3d import Axes3D
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
import numpy as np


def scatter(axes, points, color, linewidth=1):
    """Do a 3D scatter plot with the given points.

    Parameters
    ----------
    axes : mpl_toolkits.mplot3d.Axes3D
    points : tuple of np.ndarray (shape = (3,))
    color : str
    linewidth : int

    Example
    -------
    >>> fig = plt.figure()
    >>> axes = Axes3D(fig)
    >>> pts = (np.array([5.7, 3.4, 4.5]), np.array([0.2, 3.7, 3.5]))
    >>> scatter(axes, pts, 'r', 4)
    """
    # we need to have the coordinates as 3 ndarrays (x,y,z):
    x, y, z = np.asarray(zip(points[0], points[1]))
    axes.scatter(x, y, z, zdir='z', c=color, linewidth=linewidth)


def line(axes, points, color, linewidth=1):
    """Plot a line in 3D from the given points.

    Parameters
    ----------
    axes : mpl_toolkits.mplot3d.Axes3D
    points : tuple of np.ndarray (shape = (3,))
    color : str
    linewidth : int

    Example
    -------
    >>> fig = plt.figure()
    >>> axes = Axes3D(fig)
    >>> pts = (np.array([5.7, 3.4, 4.5]), np.array([0.2, 3.7, 3.5]))
    >>> line(axes, pts, 'r', 4)
    """
    # we need to have the coordinates as 3 ndarrays (x,y,z):
    x, y, z = np.asarray(zip(points[0], points[1]))
    axes.plot(x, y, z, zdir='z', c=color, linewidth=linewidth)


def maxdist(axes, maxdist_points):
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
    >>> maxdist(axes, (point1, point2))
    (array([ 87.4405 ,  56.8975 ,  -1.04535]), 48.051765744975484)
    """
    scatter(axes, maxdist_points, 'r', linewidth=18)
    for i in (0, 1):
        axes.text(*maxdist_points[i], color='blue',
            s='   (%s | %s | %s)' % (maxdist_points[i][0],
            maxdist_points[i][1], maxdist_points[i][2]))
    # draw connection line between points:
    line(axes, maxdist_points, 'y')
    # calculate length and add label:
    pos = maxdist_points[1] + ((maxdist_points[0] - maxdist_points[1]) / 2)
    dist = np.linalg.norm(maxdist_points[0] - maxdist_points[1])
    axes.text(pos[0], pos[1], pos[2], color='blue', s='%.2f' % dist)
    return (pos, dist)


def label_axes(axes, labels):
    """Label the axes of a 3D plot.

    Parameters
    ----------
    axes : mpl_toolkits.mplot3d.Axes3D
    labels : list(str)

    Example
    -------
    >>> fig = plt.figure()
    >>> axes = Axes3D(fig)
    >>> labels = ['x', 'y', 'z']
    >>> label_axes(axes, labels)
    """
    axes.set_xlabel(labels[0])
    axes.set_ylabel(labels[1])
    axes.set_zlabel(labels[2])


def set_minmax(axes, pts3d):
    """Determine min and max coordinates and set limits.

    Parameters
    ----------
    axes : mpl_toolkits.mplot3d.Axes3D
    pts3d : Points3D

    Returns
    -------
    (cmin, cmax)
    cmin, cmax : np.array (shape = (3,))
    """
    data = pts3d.get_coords()
    cmin = data.min(axis=0)
    cmax = data.max(axis=0)
    axes.set_xlim3d(cmin[0], cmax[0])
    axes.set_ylim3d(cmin[1], cmax[1])
    axes.set_zlim3d(cmin[2], cmax[2])
    return cmin, cmax


def filaments(axes, pts3d):
    """Draw edges along a filament pointlist.

    Parameters
    ----------
    axes : mpl_toolkits.mplot3d.Axes3D
    pts3d : Points3D
    """
    data = pts3d.get_coords()
    adjacent = sort_neighbors(pts3d.get_edm())
    log.debug(adjacent)
    for pair in build_tuple_seq(adjacent, cyclic=True):
        coords = [data[pair[0]], data[pair[1]]]
        line(axes, coords, 'm')


def edges(axes, pts3d):
    """Plot edges of a Points3D object.

    Parameters
    ----------
    axes : mpl_toolkits.mplot3d.Axes3D
    pts3d : Points3D
    """
    data = pts3d.get_coords()
    colors = ['r', 'g', 'b', 'y', 'c', 'm']
    for i, pair in enumerate(pts3d.edges):
        coords = [data[pair[0]], data[pair[1]]]
        curcol = colors[i % 6]
        line(axes, coords, curcol)


def triangles(axes, pts3d):
    """Plot triangles from a Points3D vertex list.

    Parameters
    ----------
    axes : mpl_toolkits.mplot3d.Axes3D
    pts3d : Points3D
    """
    rgb = lambda arg: colorConverter.to_rgba(arg, alpha=0.6)
    colors = ['r', 'g', 'b', 'y', 'c', 'm']
    for i, vtx in enumerate(pts3d.get_vertices()):
        curcol = colors[i % 6]
        tri = Poly3DCollection([vtx], facecolors=rgb(curcol), linewidth=0)
        tri.set_alpha(0.8)
        axes.add_collection3d(tri)


def junction(pts3d, show, export, stats=False, plotraw=False):
    """Create a 3D plot of a junction object.

    Parameters
    ----------
    pts3d : Points3D
    show : bool
        Whether to display the plot on the screen.
    export : str
        Path where to place a series of PNG files.
    stats : bool (optional)
        Show additional statistics in the plot.
    plotraw : bool (optional)
        Plot the raw filament points.
    """

    # prepare the figure
    fig = plt.figure()
    axes = Axes3D(fig)
    (cmin, _) = set_minmax(axes, pts3d)
    label_axes(axes, ('X', 'Y', 'Z'))

    if stats:
        # print overall area and maximum tesselation edge length:
        axes.text(cmin[0], cmin[1], cmin[2],
            s='  overall area: %.2f' % pts3d.get_area(),
            color='blue')
        axes.text(*pts3d.get_longest_edge_pos(), color='blue',
            s='  longest edge: %.2f' % pts3d.get_longest_edge())

    if plotraw:
        # draw the raw filament points:
        scatter(axes, pts3d.get_coords(), 'w')

    maxdist(axes, pts3d.get_mdpair_coords())
    filaments(axes, pts3d)
    edges(axes, pts3d)
    triangles(axes, pts3d)

    if export:
        export_pngseries(export, axes)
    if show:
        plt.show()


def export_pngseries(outdir, axes):
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


def show_3d():
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
    print('Running doctest on file "%s".' % __file__)
    import doctest
    doctest.testmod()
