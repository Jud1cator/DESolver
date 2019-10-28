import numpy as np

from NumericalMethods.num_method import NumericalMethod, get_interval


class RungeKutta(NumericalMethod):

    def __init__(self, func):
        super().__init__(func)

    def solve(self, x_start, y_start, x_end, step):
        x = get_interval(x_start, x_end, step)
        y = np.zeros(len(x))
        y[0] = y_start
        for i in range(1, len(x)):
            k1 = self.f(x[i-1], y[i-1])
            k2 = self.f(x[i-1]+step/2, y[i-1]+k1*step/2)
            k3 = self.f(x[i-1]+step/2, y[i-1]+k2*step/2)
            k4 = self.f(x[i-1]+step, y[i-1]+k3*step)
            y[i] = y[i-1] + (k1+2*k2+2*k3+k4)*step/6
        return x, y

