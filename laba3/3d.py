from mpl_toolkits import mplot3d
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D


def func(x, y):
    return (1 - x)**2 + 100 * (y - x**2)**2

x, y = np.mgrid[-4:4:20j, -4:4:10j]
z = func(x, y)
fig = plt.figure()
ax = fig.gca(projection='3d')
ax.plot_surface(x, y, z)
ax.view_init(30, 45)

plt.show()