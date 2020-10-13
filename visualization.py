import numpy as np
import matplotlib.pyplot as plt
from matplotlib import pylab
from config import *


def visualization_init():
    fig = pylab.gcf()
    fig.canvas.set_window_title('Particle Filter')


def displayParticals(p: np.ndarray, w: np.ndarray,
                     gt: np.ndarray, pause_time: float = 0.1):
    xs = np.array([r.x for r in p])
    ys = np.array([r.y for r in p])

    plt.clf()
    lm = np.array(landmarks)
    plt.plot(lm[:, 0], lm[:, 1], 'rX')

    plt.scatter(xs, ys, s=w)

    m_x = np.average(xs, weights=w)
    m_y = np.average(ys, weights=w)
    plt.plot(m_x, m_y, 'yX')
    plt.plot(gt[0], gt[1], 'gX')

    plt.legend(['LandMarks', 'Estimation', 'GT', 'Particles'], loc=2)
    plt.xlim(-100, 200)
    plt.ylim(-100, 200)
    plt.xlabel('Meters')
    plt.ylabel('Meters')
    plt.pause(pause_time)
