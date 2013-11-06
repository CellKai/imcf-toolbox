# coding: utf-8

import imaris_xml
import numpy as np

dim_x = 256
dim_y = dim_x

fh = open('spots_red_multi_ws-all.xml', 'r')
xmldata = imaris_xml.ImarisXML(fh)
    
coords = xmldata.coordinates('Position')
coords_2d = coords[:,0:2]

# normalize
coords_2d[:,0] -= coords_2d[:,0].min()
coords_2d[:,1] -= coords_2d[:,1].min()

xmax = coords_2d[:,0].max()
ymax = coords_2d[:,1].max()

matrix = np.zeros((dim_x, dim_y))
for point in coords_2d:
    pix_x = int((point[0] / xmax) * (dim_x - 1))
    pix_y = int((point[1] / ymax) * (dim_y - 1))
    # print "(%f,%f) -> (%i,%i)" % (point[0], point[1], pix_x, pix_y)
    matrix[pix_x, pix_y] += 50
    
np.savetxt('bitmap.csv', matrix, fmt='%i')
