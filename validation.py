from math import *

tolerance_xy = 15.0  # Tolerance for localization in the x and y directions.
tolerance_orientation = 0.25  # Tolerance for orientation.
# --------
#
# The following code prints the measurements associated
# with generate_ground_truth
#

def print_measurements(Z):
    T = len(Z)

    print('measurements = [[%.8s, %.8s, %.8s, %.8s],' % \
          (str(Z[0][0]), str(Z[0][1]), str(Z[0][2]), str(Z[0][3])))
    for t in range(1, T - 1):
        print(
            '                [%.8s, %.8s, %.8s, %.8s],' % \
            (str(Z[t][0]), str(Z[t][1]), str(Z[t][2]), str(Z[t][3])))
    print(
        '                [%.8s, %.8s, %.8s, %.8s]]' % \
        (str(Z[T - 1][0]), str(Z[T - 1][1]), str(Z[T - 1][2]), str(Z[T - 1][3])))


# --------
#
# The following code checks to see if your particle filter
# localizes the robot to within the desired tolerances
# of the true position. The tolerances are defined at the top. It
# might fail with small probability
#
def check_output(final_robot, estimated_position):
    error_x = abs(final_robot.x - estimated_position[0])
    error_y = abs(final_robot.y - estimated_position[1])
    error_orientation = abs(final_robot.orientation - estimated_position[2])
    error_orientation = (error_orientation + pi) % (2.0 * pi) - pi
    correct = error_x < tolerance_xy and error_y < tolerance_xy \
              and error_orientation < tolerance_orientation
    return correct

