import random

import numpy as np
import matplotlib.pyplot as plt
import time
from random import randint
import matplotlib.pyplot as plt
import matplotlib
import shapely
from shapely.geometry.point import Point
from shapely.geometry import Polygon

matplotlib.use('TkAgg')

from matplotlib.animation import FuncAnimation

fig = plt.figure()
fig.set_dpi(100)
fig.set_size_inches(7, 6.5)
circle_rad = 3

ax = plt.axes(xlim=(-5, 15), ylim=(-5, 15))
patch = plt.Circle((5, -5), circle_rad, fc='y')
rectangle = plt.Rectangle((0, 0), 3, 3)
rectangle2 = plt.Rectangle((0, 7), 3, 3)
rectangle3 = plt.Rectangle((7, 7), 3, 3)
rectangle4 = plt.Rectangle((7, 0), 3, 3)

moved_x = random.randint(-1500, 1500) / 100
moved_y = random.randint(-1500, 1500) / 100
def init():
    ax.add_patch(patch)
    ax.add_patch(rectangle)
    ax.add_patch(rectangle2)
    ax.add_patch(rectangle3)
    ax.add_patch(rectangle4)

    return patch

p1 = Polygon([(0, 0), (3, 0),(3, 3),  (0, 3)])
p2 = Polygon([(0, 10), (3, 10), (3, 7), (0, 7)])
p3 = Polygon([(7, 10), (10, 10), (10, 7), (7, 7)])
p4 = Polygon([(10, 0), (10, 3), (7, 3), (7, 0)])



patch.center = (moved_x, moved_y)
run = 0
data_x =[]
data_y =[]
steps = 150
def animate(i):
    rectangle.set_alpha(.99, )
    rectangle2.set_alpha(.99, )
    rectangle3.set_alpha(.99, )
    rectangle4.set_alpha(.99, )
    moved_x, moved_y = patch.center
    if i == steps-1:
        moved_x = random.randint(-500, 1500) / 100
        moved_y = random.randint(-500, 1500) / 100
        data_x.clear()
        data_y.clear()

    data_x.append(moved_x)
    data_y.append(moved_y)
    plt.plot(data_x, data_y, color="blue")

    p = Point(moved_x, moved_y)
    circle = p.buffer(circle_rad*2)
    # print(list(circle.exterior.coords))
    # print(circle.intersection(p2).area)
    ll_over = p1.intersection(circle).area
    ul_over = p2.intersection(circle).area
    ur_over = p3.intersection(circle).area
    lr_over = p4.intersection(circle).area
    tol = .1
    cover_tol = .4
    move = .1

    top_diff = abs((ul_over + ur_over) - (ll_over + lr_over))
    bot_diff = abs((ll_over+ul_over) - (ur_over+lr_over))
    if (top_diff < cover_tol) and bot_diff < cover_tol:
        return
    if (ul_over + ur_over) - (ll_over + lr_over) < tol:
        moved_y += move
    if (ul_over + ur_over) - (ll_over + lr_over) > tol:
        moved_y -= move

    if (ll_over+ul_over) - (ur_over+lr_over) < tol:
        moved_x -= move
    if (ll_over+ul_over) - (ur_over+lr_over) > tol:
        moved_x += move







    patch.center = (moved_x, moved_y)



    # print(val)

    return patch,


def percentage_area():
    pass


anim = FuncAnimation(fig, animate,
                     init_func=init,
                     frames=steps,
                     interval=1,
                     blit=False)

plt.show()
