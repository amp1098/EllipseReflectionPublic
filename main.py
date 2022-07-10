import math
import numpy as np
import pandas as pd
import time


# quadratic solver, display first or second solution by typing quadsolv(a, b, c)[0] or quadsolv(a, b, c)[1]
def quad_solve(a, b, c):
    sol1 = (-b + math.sqrt(b ** 2 - 4 * a * c)) / (2 * a)
    sol2 = (-b - math.sqrt(b ** 2 - 4 * a * c)) / (2 * a)
    return [sol1, sol2]


# impact parameter resolver, arguments are velocity, angle, horizontal initial position and vertical initial position
def impact(vel, theta, x, y, h):
    return max(quad_solve(
        (vel ** 2 * (np.cos(theta)) ** 2) / (h ** 2) + vel ** 2 * (np.sin(theta)) ** 2,
        (2 * vel * x * np.cos(theta)) / (h ** 2) + 2 * vel * y * np.sin(theta),
        (x ** 2) / (h ** 2) + y ** 2 - 1)
    )


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

    # if -1 > ((vel * np.cos(theta) * impact(vel, theta, x, y, h) + x) / h) or \
    #         ((vel * np.cos(theta) * impact(vel, theta, x, y, h) + x) / h) > 1:
    #     print(((vel * np.cos(theta) * impact(vel, theta, x, y, h) + x) / h))

def ell_param(vel, theta, x, y, h):
    # annoying floating point issue: sometimes the argument variable is outside the domain of arccosine, which cannot
    # actually happen unless floating point arithmetic is used. Here, I map the erroneous inputs to 1 and -1 based on
    # which value they are closest to. An example value was -1.0000000002, so -1 is fine.
    argument = (vel * np.cos(theta) * impact(vel, theta, x, y, h) + x) / h
    if argument > 1:
        result = sign(vel * np.sin(theta) * impact(vel, theta, x, y, h) + y) \
                 * math.acos(1)
    elif argument < -1:
        result = sign(vel * np.sin(theta) * impact(vel, theta, x, y, h) + y) \
                 * math.acos(-1)
    else:
        result = sign(vel * np.sin(theta) * impact(vel, theta, x, y, h) + y) \
                 * math.acos(argument)
    return result



# now we define a function to find the tangent angle at that point on the ellipse (uses atan2, a secret trig function)
def ell_tan(vel, theta, x, y, h):
    return math.atan2(
        np.cos(ell_param(vel, theta, x, y, h)),
        - h * np.sin(ell_param(vel, theta, x, y, h))
    )


# and now the best part: we define the function to find the angle of reflection, allowing us to automate this garbage
def ang_ref(vel, theta, x, y, h):
    return 2 * ell_tan(vel, theta, x, y, h) - theta


# helpful distance function
def dist(x1, x2, y1, y2):
    return np.sqrt(
        (x2-x1) ** 2 + (y2-y1) ** 2
    )


# Interesting parametric spiral
# check desmos graph to better visualize the spiral you wish to make: https://www.desmos.com/calculator/hvh9kqoqmv
# the horiz_vert parameter just tells the code to use the horizontal or vertical component
def spiral(velocity, translation, scale, travel, growth, density, param, horiz_vert):
    if horiz_vert == "horiz":
        return scale * np.exp(velocity * growth * param) * \
               np.cos(velocity * density * param) - travel * param + translation
    elif horiz_vert == "vert":
        return scale * np.exp(velocity * growth * param) * np.sin(velocity * density * param) - translation
    else:
        print("Make sure the horiz_vert paramter is a string that says either horiz or vert")
        exit()


# even/odd function, too lazy to lookup builtin
def even(number):
    if number % 2 == 0:
        return True
    elif number % 2 != 0:
        return False
    else:
        print("Error in the even() function, likely a non-numerical input or something.")



