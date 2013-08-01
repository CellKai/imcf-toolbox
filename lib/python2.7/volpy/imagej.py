#!/usr/bin/python

"""ImageJ related stuff like reading measurement results, etc."""

import numpy as np
import volpy as vp
import csv
import misc
from log import log


def read_csv_com(fname):
    """Read center-of-mass coordinates from an ImageJ CSV export.

    Parameters
    ----------
    fname : str or filehandle
        The CSV export from an ImageJ measurement. Needs to contain the results
        for center-of-mass ('XM' and 'YM' columns). Make sure to set the output
        option in ImageJ to either '.csv' or '.xls' but *NOT* '.csv' as the
        latter will use tabs as delimiter.

    Returns
    -------
    coords : np.array (shape=(N, 2))
        A numpy array containing the X and Y coordinates read from the CSV.
    """
    log.info('Reading measurements export file...')
    roi_tmp = []
    # NOTE: DictReader provides a "fieldnames" option, but unfortunately the
    # ImageJ is so lazy that not every column gets labeled, (i.e. the first
    # one) - thus we can't use it but need to assemble the structure ourselves
    roi_reader = csv.DictReader(misc.check_filehandle(fname))
    for item in roi_reader:
        roi_tmp.append([item['XM'], item['YM']])
    coords = np.array(roi_tmp, dtype=float)
    log.debug(coords)
    log.info('Done.')
    return coords


class WingJStructure(object):

    """Object representing the structures segmented by WingJ.

    WingJ produces three structure files that can be exported as CSV files,
    containing the coordinates for the A-P, the V-D, and the contour line
    separation. This class reads those files and provides various methods to
    operate on these structures.
    """

    def __init__(self, files, calib=1.0):
        """Read the CSV files and calibrate them."""
        log.info('Reading WingJ CSV files...')
        self.data = {}
        self._read_wingj_files(files)
        # data['XX'].shape = (M, 2)
        # calibrate the WingJ data if requested:
        self.data['AP'] *= calib
        self.data['VD'] *= calib
        self.data['CT'] *= calib
        log.info('Done.')

    def _read_wingj_files(self, files, delimiter='\t'):
        self.data['AP'] = np.loadtxt(files[0], delimiter=delimiter)
        self.data['VD'] = np.loadtxt(files[1], delimiter=delimiter)
        self.data['CT'] = np.loadtxt(files[2], delimiter=delimiter)

    def dist_to_structures(self, coords):
        """Calculate distance of given coordinates to WingJ structure.

        Parameters
        ----------
        coords : np.array (shape=(N, 2))
            2D coordinates given as numpy array.

        Returns
        -------
        distances : dict(edm)
            A dict containing three partial EDM's, one for each structure. Each
            of them has the shape (N, M), where N corresponds to the entries in
            the "coords" array and M corresponds to the entries in the WingJ
            data structures.
        """
        edm = {}
        log.info('Calculating distance matrices for all objects...')
        edm['AP'] = vp.dist_matrix(np.vstack([coords, self.data['AP']]))
        edm['VD'] = vp.dist_matrix(np.vstack([coords, self.data['VD']]))
        edm['CT'] = vp.dist_matrix(np.vstack([coords, self.data['CT']]))
        # edm['XX'].shape (N+M, N+M)
        log.info('Done.')

        # number of objects from coordinates file
        count = coords.shape[0]
        # slice distance matrices: the rows for all object points ([:count,:])
        # and the columns for the WingJ structure points ([:,count:])
        edm['AP'] = edm['AP'][:count, count:]
        edm['VD'] = edm['VD'][:count, count:]
        edm['CT'] = edm['CT'][:count, count:]
        # edm['XX'].shape = (N, M)
        # log.debug('Distances to "AP" structure:\n%s' % edm['AP'])
        # log.debug('Distances to "VD" structure:\n%s' % edm['VD'])
        # log.debug('Distances to "CT" structure:\n%s' % edm['CT'])
        return edm

    def min_dist_to_structures(self, coords):
        """Find minimal distances of coordinates to the WingJ structures.

        By using the dist_to_structures() result, we can just iterate through
        all rows finding the minimum and we get the shortest distance for
        each point to one of the WingJ structures.

        Parameters
        ----------
        coords : np.array (shape=(N, 2))
            2D coordinates given as numpy array.

        Returns
        -------
        mindists : dict(np.array (shape=(N, 1)))
            A dictionary with the arrays containing the minimal distance of a
            coordinate pair to the WingJ structure.
        """
        count = coords.shape[0]
        dists = self.dist_to_structures(coords)
        mindists = {}
        log.info('Finding shortest distances...')
        mindists['AP'] = np.zeros((count))
        mindists['VD'] = np.zeros((count))
        mindists['CT'] = np.zeros((count))
        for i in range(count):
            mindists['AP'][i] = dists['AP'][i].min()
            mindists['VD'][i] = dists['VD'][i].min()
            mindists['CT'][i] = dists['CT'][i].min()
        log.info('Done.')
        return mindists

    def min_dist_csv_export(self, coords, files_out):
        """Calculate minimal distances and export them to CSV."""
        mindists = self.min_dist_to_structures(coords)
        # export the results as CSV files
        log.info('Writing "%s".' % misc.filename(files_out[0]))
        np.savetxt(files_out[0], mindists['AP'], fmt='%.5f', delimiter=',')
        log.info('Writing "%s".' % misc.filename(files_out[1]))
        np.savetxt(files_out[1], mindists['VD'], fmt='%.5f', delimiter=',')
        log.info('Writing "%s".' % misc.filename(files_out[2]))
        np.savetxt(files_out[2], mindists['CT'], fmt='%.5f', delimiter=',')
