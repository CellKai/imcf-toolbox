#!/usr/bin/env python

"""
3D test script.
"""

from mpl_toolkits.mplot3d import Axes3D
import numpy as np
import matplotlib.pyplot as plt

fig = plt.figure()
ax = fig.gca(projection='3d')

x = np.random.sample(20)
y = np.random.sample(20)
z = np.random.sample(20)

ax.scatter(x,y,0,zdir='y', c='k')
plt.show()

