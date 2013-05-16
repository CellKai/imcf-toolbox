#!/usr/bin/python

'''
Process results of WingJ (http://www.tschaffter.ch/) with Imaris objects
(exported from the statistics part to XML) to do distance calculations.
'''

from log import log
import numpy as np
import volpy as vp
import ImsXMLlib
import sys
import argparse

def wingj_dist_to_surfaces(file_ap, file_vd, file_cnt, file_xml, px_size):
    '''Calculate distances from WingJ structures to Imaris objects.

    Takes the three structure files exported from WingJ containing the A-P,
    the V-D, and the contour line separation coordinates plus an XML file
    generated with Imaris containing objects with coordinates (the "Position"
    table) and calculates the closest distance from any Imaris object to each
    of the WingJ structures.

    Parameters
    ----------
    file_ap, file_vd, file_cnt : file object
        Open file handles for the three WingJ structure files.
    file_xml : file object
        An open file handle to the Imaris XML export.
    px_size : float
        The size of one pixel to correct WingJ coordinates with.

    Returns
    -------
    Nothing, currently results are written to CSV directly.
    TODO: check for existing files, ask for filenames to export to.
    '''
    # read in the WingJ CSV files
    structure_ap = np.loadtxt(file_ap, delimiter='\t')
    structure_vd = np.loadtxt(file_vd, delimiter='\t')
    structure_cnt = np.loadtxt(file_cnt, delimiter='\t')
    # structure_XX.shape (N, 2)

    xmldata = ImsXMLlib.ImarisXML(file_xml)
    wingpoints = np.array(xmldata.coordinates('Position'))
    # we're working on a projection, so we need to remove the third dimension/column
    wingpoints_2d = np.delete(wingpoints, 2, 1)
    # number of object coordinates from Imaris
    wp_nr = wingpoints_2d.shape[0]
    # wp_nr = M

    # calibrate WingJ data
    # px_size = 0.378
    structure_ap *= px_size
    structure_vd *= px_size
    structure_cnt *= px_size

    # calculate the distance matrices for all combinations
    dists_ap = vp.dist_matrix(np.vstack([wingpoints_2d, structure_ap]))
    dists_vd = vp.dist_matrix(np.vstack([wingpoints_2d, structure_vd]))
    dists_cnt = vp.dist_matrix(np.vstack([wingpoints_2d, structure_cnt]))
    # dists_XX.shape (N+M, N+M)

    # slice the desired parts from the distance matrices: just the rows for all
    # Imaris points ([:wp_nr,:]) and the columns for the WingJ points ([:,wp_nr:])
    wp_to_ap = dists_ap[:wp_nr, wp_nr:]
    wp_to_vd = dists_vd[:wp_nr, wp_nr:]
    wp_to_cnt = dists_cnt[:wp_nr, wp_nr:]
    #  wp_to_XX.shape (M, N)

    # now we can just iterate through all rows finding the minimum and we get the
    # shortest distance for each point to one of the WingJ structures:
    wp_to_ap_min = np.zeros((wp_nr))
    wp_to_vd_min = np.zeros((wp_nr))
    wp_to_cnt_min = np.zeros((wp_nr))
    for i in range(wp_nr):
        wp_to_ap_min[i] = wp_to_ap[i].min()
        wp_to_vd_min[i] = wp_to_vd[i].min()
        wp_to_cnt_min[i] = wp_to_cnt[i].min()

    # export the results as CSV files
    np.savetxt('wt1-to-AP.csv', wp_to_ap_min, delimiter=',')
    np.savetxt('wt1-to-VD.csv', wp_to_vd_min, delimiter=',')
    np.savetxt('wt1-to-contour.csv', wp_to_cnt_min, delimiter=',')

def main():
    argparser = argparse.ArgumentParser(description=__doc__)
    argparser.add_argument('--ap', required=True, type=file,
        help='WingJ structure file for the A-P separation.')
    argparser.add_argument('--vd', required=True, type=file,
        help='WingJ structure file for the V-D separation.')
    argparser.add_argument('--contour', required=True, type=file,
        help='WingJ structure file for the contour line.')
    argparser.add_argument('--imsxml', required=True, type=file,
        help='Imaris Excel XML export containing a "Position" sheet.')
    argparser.add_argument('-p', '--pixelsize', required=False, type=float,
        default=1.0, help='Pixel size to calibrate WingJ data.')
    argparser.add_argument('-v', '--verbosity', dest='verbosity',
        action='count', default=0)
    try:
        args = argparser.parse_args()
    except IOError as e:
        argparser.error(str(e))

    # default loglevel is 30 while 20 and 10 show more details
    loglevel = (3 - args.verbosity) * 10
    log.setLevel(loglevel)

    wingj_dist_to_surfaces(args.ap, args.vd,
        args.contour, args.imsxml, args.pixelsize)


if __name__ == "__main__":
        sys.exit(main())
