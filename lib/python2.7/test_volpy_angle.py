#!/usr/bin/python

'''Test script for angle_2d() from the "volpy" module.'''

import volpy as vp
import numpy as np

print
x = np.array([[1,0],[1,0]])
print x
print vp.angle_2d(x[0], x[1])

print
x = np.array([[1,0],[0,1]])
print x
print vp.angle_2d(x[0], x[1])

print
x = np.array([[1,1],[1,-1]])
print x
print vp.angle_2d(x[0], x[1])

print
x = np.array([[3,0.6],[-3,-0.0]])
print x
print vp.angle_2d(x[0], x[1])

print
x = np.array([[-3,-0.1],[1,6]])
print x
print vp.angle_2d(x[0], x[1])

print
x = np.array([[1,0],[-1,0]])
print x
print vp.angle_2d(x[0], x[1])
