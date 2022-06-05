import math
import matplotlib.pyplot as plt
import numpy as np
import sys
import csv
from numpy import random
import tkinter as tk

# I can color rays differently if they are pointing in a certain direction to show how angles play a role in the curves
# formed (maybe break up the angle array into 90 degree segments and color each segment a different color?)

# if I store all the data as its calculated prior to plotting it as a figure, and only plot at the very end, it may go
# faster

# Set values to test values
Test = 1

# Test = int(input("Debug mode?: "))

# The code below sets all the parameters used in my code. User inputs off for now

if Test == 0:
    print(Test)
    v = float(input("Initial speed? (doesn't change ray simulation, only affects particle sim): "))
    angle_min = float(input("Lower bound for rendered angles?: "))
    angle_max = float(input("Upper bound?: "))
    partition = int(input("How many partitions? (don't do more than a few thousand): "))
    angles = np.linspace((angle_min * np.pi) / 180, (angle_max * np.pi) / 180, partition)

    j = float(input("Initial horizontal position?: "))
    # figure out how to limit user input to only values within the y values above and below the previous j value
    k = float(input("Initial vertical position?: "))

    # ellipse parameter, describes horizontal scaling factor

    h = float(input("How wide is the ellipse?: "))

    # number of reflections

    R = int(input("How many reflections should you calculate?: "))

    # render only final reflection? (0 for no, 1 for yes)

    C = int(input("Render only final reflection? 1 for yes, 0 for no: "))

    # render starting point? (0 for no, 1 for yes)

    S = int(input("Render starting point? 1 for yes, 0 for no: "))

    # ray width, 0.0001 is good for large amounts of them
    # and 0.005 is good for a few of them

    W = float(input("How wide should the rays be? 0.0001 is good for many rays, and about 0.005 is good for a few. : "))

    D = int(input("Should the rays get less bright over time? (should be off if only looking at final reflections): "))

    F = int(input("Display foci?: "))

elif Test == 1:
    v = 1
    angle_min = 0
    angle_max = 360
    partition = 1000
    j = 1
    k = 0
    h = 1
    R = 2
    C = 0
    S = 1
    W = 0.0001
    D = 0
    F = 0
    angles = np.linspace((angle_min * np.pi) / 180, (angle_max * np.pi) / 180, partition)

# random angles, kinda neat
# def rand_array():
#     r = partition
#     rand_angles = []
#     while r > 0:
#         rand_angles.append(2 * np.pi * random.rand())
#         r -= 1
#     return rand_angles


# angles = rand_array()


# --- warning block in case the data is potentially too intense ---


def warning():
    if (partition >= 2000) or (partition >= 500 and R >= 50) or (R >= 500):
        print("WARNING, POTENTIALLY LARGE LOADING TIMES OR CRASHES MAY OCCUR!")
        answer = input("Halt program? (y/n): ")

        if answer == "y" or "Y":
            sys.exit()




warning()

# --- actual code occurs here ---

# foci finder / plotter


def foci(b):
    if b > 1:
        plt.plot(np.sqrt(b ** 2 - 1), 0, marker='o', markerfacecolor='green', markersize=2)
        plt.plot(-np.sqrt(b ** 2 - 1), 0, marker='o', markerfacecolor='green', markersize=2)
    if b < 1:
        plt.plot(0, np.sqrt(1 - b ** 2), marker='o', markerfacecolor='green', markersize=2)
        plt.plot(0, -np.sqrt(1 - b ** 2), marker='o', markerfacecolor='green', markersize=2)
    if b == 1:
        plt.plot(0, 0, marker='o', markerfacecolor='green', markersize=2)


# quadratic solver, display first or second solution by typing quadsolv(a, b, c)[0] or quadsolv(a, b, c)[1]


def quad_solve(a, b, c):
    sol1 = (-b + math.sqrt(b ** 2 - 4 * a * c)) / (2 * a)
    sol2 = (-b - math.sqrt(b ** 2 - 4 * a * c)) / (2 * a)
    return [sol1, sol2]

# impact parameter resolver, arguments are velocity, angle, horizontal initial position and vertical initial position


def impact(vel, theta, x, y):
    return max(quad_solve(
        (vel ** 2 * (np.cos(theta)) ** 2) / (h ** 2) + vel ** 2 * (np.sin(theta)) ** 2,
        (2 * vel * x * np.cos(theta)) / (h ** 2) + 2 * vel * y * np.sin(theta),
        (x ** 2) / (h ** 2) + y ** 2 - 1)
    )


# t parameter definition (how divided will it be and what is it range?)
n = 128
t1 = np.linspace(0, 2 * np.pi, n + 1)
t2 = np.linspace(0, 1, 3)

# ellipse equations

x1 = h * np.cos(t1)
y1 = np.sin(t1)

# timestep partition amount and time range
dt = 10
tmin = 0
tmax = 1
time = np.linspace(tmin, tmax, dt)

# # test ray parameters
# rh = v * np.cos(angles) * time * impact(v, angles, j, k) + j
# rv = v * np.sin(angles) * time * impact(v, angles, j, k) + k


# sign function
def sign(a):
    if a > 0:
        return 1
    if a < 0:
        return -1
    else:
        return 0


# following any impact, a tangent line's angle must be found at that point on ellipse
# made by zeppelin, btw
# first, the impact parameter along the ellipse must be found

def ell_param(vel, theta, x, y):
    return sign(v * np.sin(i) * impact(vel, theta, x, y) + y)\
        * math.acos((vel * math.cos(theta) * impact(vel, theta, x, y) + x) / h)


# now we define a function to find the tangent angle at that point on the ellipse (uses atan2, a secret trig function)

def ell_tan(vel, theta, x, y):
    return math.atan2(
        np.cos(ell_param(vel, theta, x, y)),
        - h * np.sin(ell_param(vel, theta, x, y))
    )


# and now the best part: we define the function to find the angle of reflection, allowing us to automate this garbage

def ang_ref(vel, theta, x, y):
    return 2 * ell_tan(vel, theta, x, y) - theta

# so how do I automate this? Well, there is a 1-1 mapping from each initial position/speed/angle, so the only inputs
# should be those things. I could potentially have the ellipse width (h) as an input too, but this works for now.
# I want to make a function that will take those conditions, find an impact point, impact parameter, and angle of
# reflection and then generate a new impact point and angle of reflection from the old ones as new initial conditions.
# Such a cycle would repeat forever, so I need to also describe the number of times I wish to calculate this using a
# for loop.

# decay function, used to make the rays dim after each reflection


def decay(b):
    if D == 1:
        return math.exp((b * math.log(2)) / R) - 1
    else:
        return 1


# arguments: speed, angle, x pos, y pos, number of reflections


def iterate(vel, theta, x, y, r):
    while r > 0:
        # impact parameter (basically, how will the velocity vector stretch to land on the ellipse?)
        i_param = impact(vel, theta, x, y)

        # initial vector

        V = np.array(
            [[vel * np.cos(theta) * i_param, vel * np.sin(theta) * i_param]]
        )
        # if only final reflection is allowed and more reflections need to be rendered
        if C == 1 and r > 1:
            # impact point updater
            x = v * np.cos(theta) * i_param + x
            y = v * np.sin(theta) * i_param + y

            # angle of reflection updater
            theta = ang_ref(vel, theta, x, y)

            # r value updater
            r -= 1
        # if only final reflection is allowed and a single reflection is left
        elif C == 1 and r == 1:
            # plotter
            plt.quiver(
                x, y, V[:, 0], V[:, 1], color='white',
                angles='xy', scale_units='xy', scale=1,
                headwidth=1, headlength=0,
                width=W,
                alpha=decay(r)
            )
            # impact point updater
            x = v * np.cos(theta) * i_param + x
            y = v * np.sin(theta) * i_param + y

            # angle of reflection updater
            theta = ang_ref(vel, theta, x, y)

            # r value updater
            r -= 1
        # plotting all reflections
        else:
            # plotter
            plt.quiver(
                x, y, V[:, 0], V[:, 1], color='white',
                angles='xy', scale_units='xy', scale=1,
                headwidth=1, headlength=0,
                width=W,
                alpha=decay(r)
            )
            # impact point updater
            x = v * np.cos(theta) * i_param + x
            y = v * np.sin(theta) * i_param + y

            # angle of reflection updater
            theta = ang_ref(vel, theta, x, y)

            # r value updater

            r -= 1



# --- Plotting ---

plt.style.use('dark_background')
plt.axis("Equal")
plt.grid(False)


# ellipse
plt.plot(x1, y1, color='white')

# starting location
if S == 1:
    plt.plot(j, k, marker='o', markerfacecolor='blue', markersize=5)
else:
    pass

# iterable reflections
print("Iterating rays....")

# counter for loop to show progress
count = len(angles)
initial = count


def between(a, b, c):   # tests if b is in between a and c
    if ((a < b) or (a > b)) and (b == c):
        return True
    else:
        return False


for i in angles:
    iterate(v, i, j, k, r=R)
    count -= 1
    next_count = count - 1
    if between(count, (9 * initial / 10), next_count):
        print("10% of iterations calculated...")
    elif between(count, (8 * initial / 10), next_count):
        print("20% of iterations calculated...")
    elif between(count, (7 * initial / 10), next_count):
        print("30% of iterations calculated...")
    elif between(count, (6 * initial / 10), next_count):
        print("40% of iterations calculated...")
    elif between(count, (5 * initial / 10), next_count):
        print("50% of iterations calculated...")
    elif between(count, (4 * initial / 10), next_count):
        print("60% of iterations calculated...")
    elif between(count, (3 * initial / 10), next_count):
        print("70% of iterations calculated...")
    elif between(count, (2 * initial / 10), next_count):
        print("80% of iterations calculated...")
    elif between(count, (1 * initial / 10), next_count):
        print("90% of iterations calculated...")


# plotting foci
if F == 1:
    foci(h)

# showing the plot
plt.show()