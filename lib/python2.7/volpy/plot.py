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
    print('Running doctest on file "%s".' % __file__)
    import doctest
    doctest.testmod()
