#!/usr/bin/python

'''
Python 2.7.3 (default, Apr 10 2013, 06:20:15) 
[GCC 4.6.3] on linux2
Type "help", "copyright", "credits" or "license" for more information.
>>> import numpy as np
>>> import volpy as vp
>>> import ImsXMLlib
>>> 
>>> file_ap = open('structure_A-P.txt', 'r')
>>> file_vd = open('structure_V-D.txt', 'r')
>>> file_cnt = open('structure_contour.txt', 'r')
>>> 
>>> xmldata = ImsXMLlib.ImarisXML(open('wt1.xml', 'r'))
>>> type(xmldata)
<class 'ImsXMLlib.ImarisXML'>
>>> wingpoints = xmldata.coordinates('Position')
>>> type(wingpoints)
<type 'list'>
>>> 
>>> structure_ap = np.loadtxt(file_ap, delimiter='\t')
>>> structure_vd = np.loadtxt(file_vd, delimiter='\t')
>>> structure_cnt = np.loadtxt(file_cnt, delimiter='\t')
>>> 
>>> structure_ap.shape
(1001, 2)
>>> structure_vd.shape
(1001, 2)
>>> structure_cnt.shape
(2000, 2)
>>> 
>>> 
>>> wingpoints_nd = np.array(wingpoints)
>>> wingpoints_nd[0]
array([ 187.752  ,   10.1101 ,    0.50355])
>>> wingpoints_2d = np.delete(wingpoints_nd, 2, 1)
>>> wingpoints_2d[0]
array([ 187.752 ,   10.1101])
>>> wingpoints_2d.shape
(105, 2)
>>> 
>>> 
>>> dists_ap = vp.dist_matrix(np.vstack([wingpoints_2d, structure_ap]))
>>> dists_vd = vp.dist_matrix(np.vstack([wingpoints_2d, structure_vd]))
>>> dists_cnt = vp.dist_matrix(np.vstack([wingpoints_2d, structure_cnt]))
>>> dists_ap.shape
(1106, 1106)
>>> dists_cnt.shape
(2105, 2105)
>>> 
>>> 
>>> wp_nr = wingpoints_2d.shape[0]
>>> wp_nr
105
>>> wp_to_ap = dists_ap[:wp_nr, wp_nr:]
>>> wp_to_vd = dists_vd[:wp_nr, wp_nr:]
>>> wp_to_cnt = dists_cnt[:wp_nr, wp_nr:]
>>> wp_to_cnt.shape
(105, 2000)
>>> wp_to_ap.shape
(105, 1001)
>>> wp_to_vd.shape
(105, 1001)
>>> 
>>> wp_to_ap_min = np.zeros((wp_nr))
>>> wp_to_vd_min = np.zeros((wp_nr))
>>> wp_to_cnt_min = np.zeros((wp_nr))
>>> 
>>> for i in range(wp_nr):
...     wp_to_ap_min[i] = wp_to_ap[i].min()
...     wp_to_vd_min[i] = wp_to_vd[i].min()
...     wp_to_cnt_min[i] = wp_to_cnt[i].min()
... 
>>> 
>>> np.savetxt('bla.csv', wp_to_ap_min, delimiter=',')
>>> np.savetxt('wt1-to-AP.csv', wp_to_ap_min, delimiter=',')
>>> np.savetxt('wt1-to-VD.csv', wp_to_vd_min, delimiter=',')
>>> np.savetxt('wt1-to-contour.csv', wp_to_cnt_min, delimiter=',')
'''
