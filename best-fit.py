import numpy as np
import scipy.optimize as spo
import matplotlib.pyplot as plt

csv = np.loadtxt(open("path/to/file.csv", "rb"), delimiter=",", skiprows=1)

t = csv[:,0]
a = csv[:,1]
a_error = csv[:,2]

def a_fun(t, c_w):
    m = 0 # mass
    g = 9.81 # acceleration due to gravity
    density = 1.29 # density of the air
    A = 0 # area facing the direction the body is falling in
    return g * (1 - np.tanh(np.sqrt((c_w * density * A * g) / (2 * m)) * t)**2)

popt, pcov = spo.curve_fit(a_fun, t, a, sigma=a_error)

c_w = popt[0]
c_w_stddev = np.sqrt(pcov[0][0])

print(c_w)
print(c_w_stddev)
plt.plot(t, a, label="data")
plt.plot(t, a_fun(t, c_w), label="best fit curve")
plt.legend()
plt.show()

