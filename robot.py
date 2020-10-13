import random
from math import *
from config import landmarks

world_size = 100.0  # world is NOT cyclic. Robot is allowed to travel "out of bounds"


class Robot:

    # --------
    # init:
    #    creates robot and initializes location/orientation
    #

    def __init__(self, length=20.0):
        self.x = random.random() * world_size  # initial x position
        self.y = random.random() * world_size  # initial y position
        self.orientation = random.random() * 2.0 * pi  # initial orientation
        self.length = length  # length of robot
        self.bearing_noise = 0.0  # initialize bearing noise to zero
        self.steering_noise = 0.0  # initialize steering noise to zero
        self.distance_noise = 0.0  # initialize distance noise to zero

    # --------
    # set:
    #    sets a robot coordinate
    #

    def set(self, new_x, new_y, new_orientation):

        if new_orientation < 0 or new_orientation >= 2 * pi:
            raise ValueError('Orientation must be in [0..2pi]')
        self.x = float(new_x)
        self.y = float(new_y)
        self.orientation = float(new_orientation)

    # --------
    # set_noise:
    #    sets the noise parameters
    #
    def set_noise(self, new_b_noise, new_s_noise, new_d_noise):
        # makes it possible to change the noise parameters
        # this is often useful in particle filters
        self.bearing_noise = float(new_b_noise)
        self.steering_noise = float(new_s_noise)
        self.distance_noise = float(new_d_noise)

    # --------
    # measurement_prob
    #    computes the probability of a measurement
    #

    def measurement_prob(self, measurements):

        # calculate the correct measurement
        predicted_measurements = self.sense(0)  # Our sense function took 0 as an argument to switch off noise.

        # compute errors
        error = 1.0
        for i in range(len(measurements)):
            error_bearing = abs(measurements[i] - predicted_measurements[i])
            error_bearing = (error_bearing + pi) % (2.0 * pi) - pi  # truncate

            # update Gaussian
            error *= (exp(- (error_bearing ** 2) / (self.bearing_noise ** 2) / 2.0) /
                      sqrt(2.0 * pi * (self.bearing_noise ** 2)))

        return error

    def __repr__(self):  # allows us to print robot attributes.
        return '[x=%.6s y=%.6s orient=%.6s]' % (str(self.x), str(self.y),
                                                str(self.orientation))

    # --------
    # move:
    #
    def move(self, motion):

        alpha, d = motion  # angle, distance

        B = (d / self.length) * tan(alpha)
        if (alpha < 0.001):
            x = self.x + d * cos(B + self.orientation)
            y = self.y + d * sin(B + self.orientation)
        else:
            R = d / B
            cx = self.x - sin(self.orientation) * R
            cy = self.y + cos(self.orientation) * R
            x = cx + sin(B + self.orientation) * R
            y = cy - cos(B + self.orientation) * R

        orient = (self.orientation + B)  # Calculate the new orientation

        # Add errors for the movement phase and orientation
        x += random.gauss(0.0, self.distance_noise)
        y += random.gauss(0.0, self.distance_noise)
        orient += random.gauss(0.0, self.steering_noise)  # Add error for the orientation

        # Normalize orientation
        orient %= (2 * pi)

        # Create the new robot after motion update - prediction phase
        result = Robot(self.length)
        result.set(x, y, orient)
        result.set_noise(self.bearing_noise, self.steering_noise, self.distance_noise)

        return result

    # --------
    # sense:
    #

    def sense(self, add_noise=1):  # do not change the name of this function
        Z = []

        for i in range(len(landmarks)):
            delta_y = landmarks[i][0] - self.y
            delta_x = landmarks[i][1] - self.x

            bearing = atan2(delta_y, delta_x) - self.orientation
            bearing %= (2 * pi)

            if add_noise == 1:
                bearing += random.gauss(0, self.bearing_noise)

            Z.append(bearing)

        return Z