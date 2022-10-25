import numpy as np
import matplotlib.pyplot as plt
import time
from random import randint
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('TkAgg')

from matplotlib.animation import FuncAnimation
fig = plt.figure()
fig.set_dpi(100)
fig.set_size_inches(7, 6.5)

ax = plt.axes(xlim=(0, 10), ylim=(0, 10))
patch = plt.Circle((5, -5), 1.75, fc='y')
rectangle = plt.Rectangle((0, 0), 3, 3)

def init():
    patch.center = (5, 5)
    ax.add_patch(patch)
    ax.add_patch(rectangle)
    return patch,

def animate(i):
    x, y = patch.center
    x = 5 + 3 * np.sin(np.radians(i))
    y = 5 + 3 * np.cos(np.radians(i))
    patch.center = (x, y)
    val = np.random.rand()
    rectangle.set_alpha(i/1000)
    print(val)

    return patch,

anim = FuncAnimation(fig, animate,
                               init_func=init,
                               frames=36000,
                               interval=2,
                               blit=False)

plt.show()