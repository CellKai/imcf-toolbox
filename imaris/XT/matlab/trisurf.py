from mpl_toolkits.mplot3d import Axes3D
from mpl_toolkits.mplot3d import art3d
from matplotlib import cm
import matplotlib.pyplot as plt
import numpy as np
x = np.array([1.0, 0.1, 2.9])
y = np.array([2.0, 1.1, 1.2])
z = np.array([0.0, 2.1, 4.6])
fig = plt.figure()
# ax = fig.gca(projection='3d')
# ax.plot_trisurf(x, y, z, cmap=cm.jet, linewidth=0.2)
verts = [[[-6.1,-4.1,-2.1],
    [ 2.9, 1.2, 4.6],
    [ 1.,  2.,  0. ]]]
# polyc = art3d.Poly3DCollection(verts, cmap=cm.jet, linewidth=0.2)
# colset = []
# for i in xrange(len(verts)):
#     avgzsum = verts[i,0,2] + verts[i,1,2] + verts[i,2,2]
#     colset.append(avgzsum / 3.0)
# 
# polyc.set_facecolors(colset)
# plt.show()


from mpl_toolkits.mplot3d.art3d import Poly3DCollection

ax = Axes3D(fig)
# ax = fig.gca(projection='3d')

# x = [0,1,1,0]
# y = [0,0,1,1]
# z = [0,1,0,1]
verts = [zip(x, y,z)]
print verts
poly = Poly3DCollection(verts)
poly.set_alpha(0.6)
ax.add_collection3d(Poly3DCollection(verts))

ax.set_xlim3d(0,3)
ax.set_ylim3d(1,2)
ax.set_zlim3d(0,5)
ax.set_xlabel('X')
ax.set_ylabel('Y')
ax.set_zlabel('Z')
plt.show()
