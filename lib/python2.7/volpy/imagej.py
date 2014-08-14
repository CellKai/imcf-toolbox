#!/usr/bin/python

"""ImageJ related stuff like reading measurement results, etc."""

import numpy as np
from os import sep
from os.path import join, dirname, exists
import volpy as vp
import csv
import misc
from misc import readtxt, flatten
from log import log


def read_csv_com(fname):
    """Read center-of-mass coordinates from an ImageJ CSV export.

    Read in the CSV export from an ImageJ measurement. The file needs to
    contain the results for center-of-mass ('XM' and 'YM' columns). Make sure
    to set the output option in ImageJ to either '.csv' or '.xls' but *NOT*
    '.txt' as the latter will use tabs as delimiter.

    The CSV file is required to have the above described column labels as the
    first line to identify which column contains the relevant data. Everything
    else is ignored. This is one possible example for such an export file:
    ------- 8< -------
    ,Area,Mean,Min,Max,XM,YM
    1,496,197,96,232,187.752,10.1101
    1,496,197,96,232,169.939,16.717
    1,496,197,96,232,161.114,27.0873
    ------- >8 -------

    Parameters
    ----------
    fname : str or filehandle

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
    roi_reader = csv.DictReader(misc.filehandle(fname))
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
        """Read the CSV files and calibrate them.

        Instance Variables
        ------------------
        data : dict(np.array)
        calib : float
        """
        log.info('Reading WingJ CSV files...')
        self.data = {}
        self.calib = calib
        self._read_wingj_files(files)
        # data['XX'].shape = (M, 2)
        # calibrate the WingJ data if requested:
        self.data['AP'] *= calib
        self.data['VD'] *= calib
        self.data['CT'] *= calib
        self._calc_origin()
        log.info('Done.')

    def _read_wingj_files(self, files, delimiter='\t'):
        """Read the WingJ files into our data structure."""
        # if files is not a list, we need to add the default filenames:
        if isinstance(files, str):
            filelist = []
            filelist.append(files + '/structure_A-P.txt')
            filelist.append(files + '/structure_V-D.txt')
            filelist.append(files + '/structure_contour.txt')
            files = filelist
        self.data['AP'] = np.loadtxt(files[0], delimiter=delimiter)
        self.data['VD'] = np.loadtxt(files[1], delimiter=delimiter)
        self.data['CT'] = np.loadtxt(files[2], delimiter=delimiter)

    def _calc_origin(self):
        """Calculate the origin (the intersection of A-P and V-D lines)."""
        # TODO: investigate more WingJ structure files, probably the origin
        # spot is always stored as the "central" element in the AP/VD files
        # (meaning entry 500 of 1000).
        edm = vp.dist_matrix(np.vstack([self.data['AP'], self.data['VD']]))
        closest = vp.get_min_dist_pair(edm, self.data['AP'].shape[0])
        log.debug(self.data['AP'][closest[0]])
        log.debug(self.data['VD'][closest[1] - self.data['AP'].shape[0]])
        log.debug(edm[closest])
        # *IF* the above holds, we can just use the coordinates of the first
        # spot, instead of calculating "new" coordinates:
        self.data['orig'] = self.data['AP'][closest[0]]
        log.debug('Set origin to %s.' % self.data['orig'])

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
        edm['orig'] = vp.dist_matrix(np.vstack([coords, self.data['orig']]))
        # edm['XX'].shape (N+M, N+M)
        log.info('Done.')

        # number of objects from coordinates file
        count = coords.shape[0]
        # slice distance matrices: the rows for all object points ([:count,:])
        # and the columns for the WingJ structure points ([:,count:])
        edm['AP'] = edm['AP'][:count, count:]
        edm['VD'] = edm['VD'][:count, count:]
        edm['CT'] = edm['CT'][:count, count:]
        # there is just one "orig" spot, so we just slice the first row:
        edm['orig'] = edm['orig'][0, 1:]
        # edm['XX'].shape = (N, M)
        # log.debug('Distances to "AP" structure:\n%s' % edm['AP'])
        # log.debug('Distances to "VD" structure:\n%s' % edm['VD'])
        # log.debug('Distances to "CT" structure:\n%s' % edm['CT'])
        log.debug('Distances to origin:\n%s' % edm['orig'])
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
        mindists['orig'] = dists['orig']
        for i in range(count):
            mindists['AP'][i] = dists['AP'][i].min()
            mindists['VD'][i] = dists['VD'][i].min()
            mindists['CT'][i] = dists['CT'][i].min()
        log.info('Done.')
        return mindists

    def min_dist_csv_export(self, coords, files):
        """Calculate minimal distances and export them to CSV."""
        # if "files" is a str it is a directory, so we need to assemble the
        # filelist ourselves:
        if isinstance(files, str):
            filelist = []
            filelist.append(files + '/mindists_A-P.csv')
            filelist.append(files + '/mindists_V-D.csv')
            filelist.append(files + '/mindists_contour.csv')
            filelist.append(files + '/mindists_orig.csv')
            files = filelist
        mindists = self.min_dist_to_structures(coords)
        # export the results as CSV files
        log.info('Writing "%s".' % misc.filename(files[0]))
        np.savetxt(files[0], mindists['AP'], fmt='%.5f', delimiter=',')
        log.info('Writing "%s".' % misc.filename(files[1]))
        np.savetxt(files[1], mindists['VD'], fmt='%.5f', delimiter=',')
        log.info('Writing "%s".' % misc.filename(files[2]))
        np.savetxt(files[2], mindists['CT'], fmt='%.5f', delimiter=',')
        log.info('Writing "%s".' % misc.filename(files[3]))
        np.savetxt(files[3], mindists['orig'], fmt='%.5f', delimiter=',')


def gen_tile_config(mosaic_ds, fixpath=False):
    """Generate a tile configuration for Fiji's stitcher.

    Generate a layout configuration file for a ceartain mosaic in the format
    readable by Fiji's "Grid/Collection stitching" plugin. The configuration is
    stored in a file in the input directory carrying the mosaic's index number
    as a suffix.

    Parameters
    ----------
    mosaic_ds : volpy.dataset.MosaicData
        The mosaic dataset to generate the tile config for.
    fixpath : bool
        Convert path separators in the tileconfig to current OS environment?

    Returns
    -------
    config : list(str)
        The tile configuration as a list of strings, one per line.
    """
    conf = list()
    app = conf.append
    subvol_size_z = mosaic_ds.subvol[0].get_dimensions()['Z']
    subvol_position_dim = len(mosaic_ds.subvol[0].position['relative'])
    app('# Define the number of dimensions we are working on\n')
    if subvol_size_z > 1:
        app('dim = 3\n')
        if subvol_position_dim < 3:
            coord_format = '(%f, %f, 0.0)\n'
        else:
            coord_format = '(%f, %f, %f)\n'
    else:
        app('dim = 2\n')
        coord_format = '(%f, %f)\n'
    app('# Define the image coordinates (in pixels)\n')
    for subvol in mosaic_ds.subvol:
        # this will be broken for OIF files until the FOLLOWUP_REAL_OIF_NAME
        # is fixed in the dataset module:
        line = '%s; ;' % subvol.storage['full']
        # TODO: investigate if the stitcher accepts '/' as pathsep on windows
        if(fixpath):
            line = line.replace('\\', sep)
        line += coord_format % subvol.position['relative']
        app(line)
    return conf


def gen_stitching_macro_code(experiment, pfx, path='', tplpath='', flat=False):
    """Generate code in ImageJ's macro language to stitch the mosaics.

    Take two template files ("head" and "body") and generate an ImageJ
    macro to stitch the mosaics. Using the splitted templates allows for
    setting default values in the head that can be overridden in this
    generator method (the ImageJ macro language doesn't have a command to
    check if a variable is set or not, it just exits with an error).

    Parameters
    ----------
    experiment : volpy.experiment.MosaicExperiment
        The object containing all information about the mosaic.
    pfx : str
        The prefix for the two template files, will be completed with the
        corresponding suffixes "_head.ijm" and "_body.ijm".
    path : str
        The path to use as input directory *INSIDE* the macro.
    tplpath : str
        The path to a directory or zip file containing the templates.
    flat : bool
        Used to request a flattened string instead of a list of strings.

    Returns
    -------
    ijm : list(str) or str
        The generated macro code as a list of str (one str per line) or as
        a single long string if requested via the "flat" parameter.
    """
    # TODO: generalize by supplying a dict with values to put between the head
    # and body section of the macro
    ## mcount = self.experiment['mcount']  # FIXME
    mcount = experiment.supplement['mcount']
    # by default templates are expected in a subdir of the current package:
    if (tplpath == ''):
        tplpath = join(dirname(__file__), 'ijm_templates')
        log.debug('Looking for template directory: %s' % tplpath)
        if not exists(tplpath):
            tplpath += '.zip'
            log.debug('Looking for template directory: %s' % tplpath)
    if not exists(tplpath):
        raise IOError("Template directory can't be found!")
    log.info('Template directory: %s' % tplpath)
    ijm = readtxt(pfx + '_head.ijm', tplpath)
    ijm.append('\n')

    ## ijm.append('name = "%s";\n' % self.infile['dname'])  # FIXME
    ijm.append('name = "%s";\n' % experiment.infile['dname'])
    ijm.append('padlen = %i;\n' % len(str(mcount)))
    ijm.append('mcount = %i;\n' % mcount)
    # windows path separator (in)sanity:
    path = path.replace('\\', '\\\\')
    ijm.append('input_dir="%s";\n' % path)
    ijm.append('use_batch_mode = true;\n')

    # If the overlap is below a certain level (5 percent), we disable
    # computing the actual positions and subpixel accuracy:
    ## if (self.mosaics[0]['ratio'] > 95.0):  # FIXME
    if (experiment[0].get_overlap('pct') < 5.0):
        ijm.append('compute = false;\n')

    ijm.append('\n')
    ijm += readtxt(pfx + '_body.ijm', tplpath)
    log.debug('--- ijm ---\n%s\n--- ijm ---' % ijm)
    if (flat):
        return(flatten(ijm))
    else:
        return(ijm)
