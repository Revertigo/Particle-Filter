import random
from math import *
import numpy as np
from robot import Robot
from visualization import displayParticals, visualization_init
from config import bearing_noise, steering_noise, distance_noise


def particle_filter(motions, measurements, ground_truths, N=500):
    # --------
    #
    # Make particles
    #

    p = []
    for i in range(N):
        r = Robot()
        r.set_noise(bearing_noise, steering_noise, distance_noise)
        p.append(r)

    visualization_init()
    displayParticals(p, np.ones(len(p)), ground_truths[0], 2)
    # --------
    # Update particles
    #
    for t in range(len(motions)):

        # Update weights
        # motion update (prediction)
        p2 = []
        for i in range(N):
            p2.append(p[i].move(motions[t]))
        p = p2

        # measurement update
        w = []
        for i in range(N):
            w.append(p[i].measurement_prob(measurements[t]))

        # Resampling phase
        p3 = []
        index = int(random.random() * N)
        mw = max(w)
        for i in range(N):
            beta = random.random() * 2.0 * mw
            while beta > w[index]:
                beta -= w[index]
                index = (index + 1) % N
            p3.append(p[index])
        p = p3

        displayParticals(p, w, ground_truths[t])
    return get_position(p)


def get_position(p):
    x = 0.0
    y = 0.0
    orientation = 0.0
    for i in range(len(p)):
        x += p[i].x
        y += p[i].y
        # orientation is tricky because it is cyclic. By normalizing
        # around the first particle we are somewhat more robust to
        # the 0=2pi problem
        orientation += (((p[i].orientation - p[0].orientation + pi) % (2.0 * pi))
                        + p[0].orientation - pi)
    return [x / len(p), y / len(p), orientation / len(p)]
