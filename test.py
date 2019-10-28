import numpy as np
import matplotlib.pyplot as plt

from Functions import var18
from NumericalMethods.num_method import get_interval
from NumericalMethods.Euler import Euler
from NumericalMethods.ImprovedEuler import ImprovedEuler
from NumericalMethods.RungeKutta import RungeKutta


x0 = 1
y0 = 0.5
X = 9
h = 0.1

x = get_interval(x0, X, h)
y_exact = 1/(1+x)
plt.plot(x, y_exact, label='Exact')

euler = Euler(var18.first_derivative)
x, y_e = euler.solve(x0, y0, X, h)
plt.plot(x, y_e, label='Euler')

ieuler = ImprovedEuler(var18.first_derivative)
x, y_i = ieuler.solve(x0, y0, X, h)
plt.plot(x, y_i, label='Improved Euler')

runkut = RungeKutta(var18.first_derivative)
x, y_r = runkut.solve(x0, y0, X, h)
plt.plot(x, y_r, label='Runge-Kutta')

# plt.subplot(1, 3, 1)
# plt.plot(np.arange(0, len(x)), abs(y_exact-y_e), label='Euler error')

plt.title('Function and different approximations')
plt.legend()
plt.show()

