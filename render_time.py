# The goal of this script is to estimate the render time for any animation. The process will work like this:
# 1: Gather a few data points (the more data points, the higher the accuracy)
# 2: Extrapolate future points with a spline
# 3: Estimate the total time by integrating this spline from 0 to num_final
# I may need to clean the data to remove outliers, as sudden changes in computation speed will throw off the estimation
# also how in the world do I perform a cubic spline extrapolation???

from scipy.optimize import curve_fit
import scipy.integrate as integrate
import numpy as np
import matplotlib.pyplot as plt


def reject_outliers(data, m=2.):  # data must be a numpy array, if number is 2 * std dev it is erased from this universe
    d = np.abs(data - np.median(data))
    mdev = np.median(d)
    s = d/mdev if mdev else 0.
    return data[s < m]


# --- defining some example functions to use in curve_fit ---
def quadratic(x, a, b, c):
    return a*x**2+b*x+c


def cubic(x, a, b, c, d):
    return a * x ** 3 + b * x ** 2 + c * x + d

#
# def expon(x, a, b ,c):
#     return a * exp(b * x) + c


# --- guessing algorithm ---
# add confidence rating based on noisiness of input
def render_guess(data, final_frame):
    filtered_data = reject_outliers(data, m=2)
    # defining x values as an array from 0 to the last value in data
    x_var = np.linspace(1, len(filtered_data), num=len(filtered_data), endpoint=True)
    # y is just the data
    y_var = filtered_data
    # curve fitting here
    params, covariance = curve_fit(quadratic, x_var, y_var)

    # the curve itself, uses some weird labmda thing that somehow makes it all work, idk
    f = lambda x: params[0] * x ** 2 + params[1] * x + params[2]

    # integration occurs here to find total estimated time
    total = integrate.quad(f, 1, final_frame, points=x_var, limit=(len(filtered_data) + 1))

    xnew = np.linspace(0, 90, num=90, endpoint=True)
    plt.plot(x_var, y_var, 'o', xnew, f(xnew), '-')
    plt.xlim(0, max(xnew))
    plt.ylim(0, max(f(xnew)))
    plt.show()

    return total[0]



