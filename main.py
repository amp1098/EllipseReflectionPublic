import math
import numpy as np


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

# timestep partition amount and time range
dt = 10
tmin = 0
tmax = 1
time = np.linspace(tmin, tmax, dt)


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

def ell_param(vel, theta, x, y, h):
    return sign(vel * np.sin(theta) * impact(vel, theta, x, y, h) + y)\
        * math.acos((vel * np.cos(theta) * impact(vel, theta, x, y, h) + x) / h)


# now we define a function to find the tangent angle at that point on the ellipse (uses atan2, a secret trig function)

def ell_tan(vel, theta, x, y, h):
    return math.atan2(
        np.cos(ell_param(vel, theta, x, y, h)),
        - h * np.sin(ell_param(vel, theta, x, y, h))
    )


# and now the best part: we define the function to find the angle of reflection, allowing us to automate this garbage

def ang_ref(vel, theta, x, y, h):
    return 2 * ell_tan(vel, theta, x, y, h) - theta

