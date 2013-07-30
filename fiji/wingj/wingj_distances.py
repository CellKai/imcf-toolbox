#!/usr/bin/python

"""
Process results of WingJ (http://www.tschaffter.ch/) with Imaris objects
(exported from the statistics part to XML) to do distance calculations.
"""

from volpy.imagej import read_csv_com
from log import log
import misc
import numpy as np
import volpy as vp
import imaris_xml as ix
import sys
import argparse


class WingJStructure(object):

    """Object representing the structures segmented by WingJ."""

    def __init__(self, files, calib=1.0):
        """Read the CSV files and calibrate them."""
        log.info('Reading WingJ CSV files...')
        self.data = {}
        self.data['AP'] = np.loadtxt(files[0], delimiter='\t')
        self.data['VD'] = np.loadtxt(files[1], delimiter='\t')
        self.data['CT'] = np.loadtxt(files[2], delimiter='\t')
        # data['XX'].shape = (M, 2)
        # calibrate the WingJ data if requested:
        self.data['AP'] *= calib
        self.data['VD'] *= calib
        self.data['CT'] *= calib
        log.info('Done.')

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


def wingj_dist_to_surfaces(files_wingj, files_out, px_size=1.0,
        file_imsxml=None, file_ijroi=None):
    """Calculate distances from WingJ structures to spots in 2D.

    Takes the three structure files exported from WingJ containing the A-P, the
    V-D, and the contour line separation coordinates plus an XML file generated
    with Imaris containing objects with coordinates (the "Position" table) or a
    CSV file generated by ImageJ containing "center of mass" coordinates and
    calculates the closest distance from any Imaris object to each of the WingJ
    structures.

    Parameters
    ----------
    files_wingj, files_out : file handles or strings
        3-tuples of file handles or strings with filenames for the WingJ
        structure files resp. the corresponding output files.
    file_imsxml, file_ijroi : file handle or string
        A file handle or filename-string to an Imaris XML export resp. the
        ImageJ measurements CSV export.
    px_size : float, optional
        The size of one pixel to correct WingJ coordinates with.

    Returns
    -------
    Nothing, all results are written to output CSV files directly.
    """
    if file_imsxml is not None:
        # create the ImarisXML object and read the 'Position' sheet
        coords = ix.ImarisXML(file_imsxml).coordinates('Position')
        # we're working on a projection, so remove the third dimension/column
        coords = np.delete(coords, 2, 1)
    elif file_ijroi is not None:
        coords = read_csv_com(file_ijroi)
    else:
        raise AttributeError('no reference file given!')

    wingj = WingJStructure(files_wingj, px_size)
    mindists = wingj.min_dist_to_structures(coords)

    # export the results as CSV files
    log.info('Writing "%s".' % misc.filename(files_out[0]))
    np.savetxt(files_out[0], mindists['AP'], delimiter=',')
    log.info('Writing "%s".' % misc.filename(files_out[1]))
    np.savetxt(files_out[1], mindists['VD'], delimiter=',')
    log.info('Writing "%s".' % misc.filename(files_out[2]))
    np.savetxt(files_out[2], mindists['CT'], delimiter=',')
    log.info('Finished.')


def main():
    """Parse commandline arguments and run distance calculations."""
    argparser = argparse.ArgumentParser(description=__doc__)
    argparser.add_argument('--ap', required=True, type=file,
        help='WingJ structure file for the A-P separation.')
    argparser.add_argument('--vd', required=True, type=file,
        help='WingJ structure file for the V-D separation.')
    argparser.add_argument('--cnt', required=True, type=file,
        help='WingJ structure file for the contour line.')
    group = argparser.add_mutually_exclusive_group(required=True)
    group.add_argument('--imsxml', type=file, default=None,
        help='Imaris Excel XML export containing a "Position" sheet.')
    group.add_argument('--ijroi', type=file, default=None,
        help='ImageJ CSV export having "center of mass" measurements.')
    argparser.add_argument('--apout', type=argparse.FileType('w'),
        required=True, help='Output CSV file for distances to A-P line.')
    argparser.add_argument('--vdout', type=argparse.FileType('w'),
        required=True, help='Output CSV file for distances to V-D line.')
    argparser.add_argument('--cntout', type=argparse.FileType('w'),
        required=True, help='Output CSV file for distances to contour line.')
    argparser.add_argument('-p', '--pixelsize', required=False, type=float,
        default=1.0, help='Pixel size to calibrate WingJ data.')
    argparser.add_argument('-v', '--verbosity', dest='verbosity',
        action='count', default=0)
    try:
        args = argparser.parse_args()
    except IOError as err:
        argparser.error(str(err))

    misc.set_loglevel(args.verbosity)

    wingj_dist_to_surfaces(
        (args.ap, args.vd, args.cnt),
        (args.apout, args.vdout, args.cntout),
        args.pixelsize, args.imsxml, args.ijroi)


if __name__ == "__main__":
    sys.exit(main())
