#!/usr/bin/python

"""ImageJ related stuff like reading measurement results, etc."""

import numpy as np
import csv
import misc
from log import log


def read_csv_com(fname):
    """Read center-of-mass coordinates from an ImageJ CSV export.

    Parameters
    ----------
    fname : str or filehandle
        The CSV export from an ImageJ measurement. Needs to contain the results
        for center-of-mass ('XM' and 'YM' columns).

    Returns
    -------
    coords : np.array (shape=(N, 2))
        A numpy array containing the X and Y coordinates read from the CSV.
    """
    log.info('Reading measurements export file...')
    roi_tmp = []
    roi_reader = csv.DictReader(misc.check_filehandle(fname))
    for item in roi_reader:
        roi_tmp.append([item['XM'], item['YM']])
    coords = np.array(roi_tmp, dtype=float)
    log.debug(coords)
    log.info('Done.')
    return coords
