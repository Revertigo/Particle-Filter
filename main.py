from math import *
import matplotlib.pyplot as plt
import numpy as np
from robot import Robot
from algorithm import particle_filter
from config import bearing_noise, steering_noise, distance_noise
from validation import print_measurements, check_output


# The following code generates ground truth to be used by the animation
def generate_ground_truth_loc(motions):
    myrobot = Robot()
    myrobot.set_noise(bearing_noise, steering_noise, distance_noise)

    Z = []
    T = len(motions)
    pos = []
    for t in range(T):
        myrobot = myrobot.move(motions[t])
        Z.append(myrobot.sense(False))
        pos.append((myrobot.x, myrobot.y))
    # print 'Robot:    ', myrobot
    return [myrobot, Z, np.array(pos)]

if __name__ == '__main__':
    number_of_iterations = 100
    motions = [[2. * pi / 18, 12.] for row in range(number_of_iterations)]

    x = generate_ground_truth_loc(motions)
    # Used for animation
    ground_truths = x[2]

    robot = x[0]
    measurements = x[1]
    estimated_position = particle_filter(motions, measurements, ground_truths)
    print_measurements(measurements)
    print('Ground truth:\t\t{}'.format(robot))
    print('Particle filter:\t{}'.format(estimated_position))
    print('Code check:\t\t\t{}'.format(check_output(robot, estimated_position)))

    plt.show()