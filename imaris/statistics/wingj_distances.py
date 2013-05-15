#!/usr/bin/python

'''
Process results of WingJ (http://www.tschaffter.ch/) with Imaris objects
(exported from the statistics part to XML) to do distance calculations.
'''

import numpy as np
import volpy as vp
import ImsXMLlib

# read in the WingJ CSV files
file_ap = open('structure_A-P.txt', 'r')
file_vd = open('structure_V-D.txt', 'r')
file_cnt = open('structure_contour.txt', 'r')
structure_ap = np.loadtxt(file_ap, delimiter='\t')
structure_vd = np.loadtxt(file_vd, delimiter='\t')
structure_cnt = np.loadtxt(file_cnt, delimiter='\t')
# structure_XX.shape (N, 2)

xmldata = ImsXMLlib.ImarisXML(open('wt1.xml', 'r'))
wingpoints = np.array(xmldata.coordinates('Position'))
# we're working on a projection, so we need to remove the third dimension/column
wingpoints_2d = np.delete(wingpoints, 2, 1)
# number of object coordinates from Imaris
wp_nr = wingpoints_2d.shape[0]
# wp_nr = M

# calibrate WingJ data
px_size = 0.378
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
