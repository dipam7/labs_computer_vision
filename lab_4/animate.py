import numpy as np
from math import *
import matplotlib
import matplotlib.pyplot as plt
import matplotlib.animation as animation

# this function gets called every time a new frame should be generated.


def takeoff(frame_number):
    global tx, ty, tz, compass, tilt, twist
    ty += 20
    if frame_number > 10: 
        tz -= 5
    if frame_number > 20:
        tilt += 0.3
    if frame_number > 38:
        tilt = pi/2

    f = 0.002
    m1 = np.identity(3) * f
    m1[2,2] = 1

    m2 = np.array([[1,0,0],
                   [0, np.cos(tilt), -np.sin(tilt)],
                   [0, np.sin(tilt), np.cos(tilt)]])

    m3 = np.array([[np.cos(twist), 0, -np.sin(twist)], 
                   [0, 1, 0], 
                   [np.sin(twist), 0, np.cos(twist)]])

    m4 = np.array([[np.cos(compass), -np.sin(compass), 0], 
                  [np.sin(compass), np.cos(compass), 0], 
                  [0, 0, 1]])

    m5 =  np.array([[1, 0, 0, tx], [0, 1, 0, ty], [0, 0, 1, tz]])

    m = np.matmul(np.matmul(np.matmul(np.matmul(m1, m2), m3), m4), m5)
    pr = []
    pc = []
    for p in pts3:
        inc = np.array([p[0], p[1], p[2], 1])
        t = np.matmul(m, inc)
        if t[2] < 0:
            pr += [t[0] / t[2] + 0.00001]
            pc += [t[1] / t[2] + 0.00001]

    plt.cla()
    plt.gca().set_xlim([-0.002, 0.002])
    plt.gca().set_ylim([-0.002, 0.002])
    line, = plt.plot(pr, pc, 'k', linestyle="", marker=".", markersize=2)
    return line,



# load in 3d point cloud
with open("airport.pts", "r") as f:
    pts3 = [[float(x) for x in l.split(" ")] for l in f.readlines()]


# initialize plane pose (translation and rotation)
(tx, ty, tz) = (0, -30, -10)
(compass, tilt, twist) = (0, pi/2, 0)

# takeoff(50)
# # create animation!
fig, ax = plt.subplots()
frame_count = 50

ani = animation.FuncAnimation(fig, takeoff, frames=range(0, frame_count))

# uncomment if you want to save your animation as a movie. :)
ani.save("movie.mp4")

# plt.show()
