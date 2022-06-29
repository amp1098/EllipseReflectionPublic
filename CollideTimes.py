import numpy as np
import math

h = 2

# Goal: To create an array that contains both every impact time of a bunch of simulated particles and pair them
# with some "particle ID", likely just an integer


def quad_solve(a, b, c):
    sol1 = (-b + math.sqrt(b ** 2 - 4 * a * c)) / (2 * a)
    sol2 = (-b - math.sqrt(b ** 2 - 4 * a * c)) / (2 * a)
    return [sol1, sol2]


def impact(vel, theta, x, y):
    return max(quad_solve(
        (vel ** 2 * (np.cos(theta)) ** 2) / (h ** 2) + vel ** 2 * (np.sin(theta)) ** 2,
        (2 * vel * x * np.cos(theta)) / (h ** 2) + 2 * vel * y * np.sin(theta),
        (x ** 2) / (h ** 2) + y ** 2 - 1)
    )


angle_min = 0
angle_max = 360
# max partition for this quick_sort is 4245, better method needed for higher res data
partition = 3000

angles = np.linspace((angle_min * np.pi) / 180, (angle_max * np.pi) / 180, partition)


#quick_sort algorithm, stolen from youtube video: https://www.youtube.com/watch?v=kFeXwkgnQ9U

def quick_sort(seq):
    length = len(seq)
    if length <= 1:
        return seq
    else:
        pivot = seq.pop()

    items_greater = []
    items_lesser = []

    for i in seq:
        if i > pivot:
            items_greater.append(i)

        else:
            items_lesser.append(i)

    return quick_sort(items_lesser) + [pivot] + quick_sort(items_greater)


def impact_times(vel, theta, J, K):
    r = len(angles)
    times = []
    while r > 0:
        r -= 1
        times.append(impact(vel, theta[r], J, K))
    return times


v = 1
j = 0.3
k = 0.2


def sort_times(vel, theta, J, K):
    return quick_sort(impact_times(vel, theta, J, K))


print(sort_times(v, angles, j, k))

# This part may be the most memory intensive part of the program, even more than the ray calculations
# I will create an array of len(impact_times) to describe the number of particles in the simulation
# and assign to each of them a velocity (magnitude and angle). The individual particle velocities will only be updated
# when each collision occurs. At the very least, I'll need to get an animation to work.


