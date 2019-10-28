import numpy as np

from NumericalMethods.num_method import NumericalMethod, get_interval


class ImprovedEuler(NumericalMethod):

    def __init__(self, f):
        super().__init__(f)

    def solve(self, x_start, y_start, x_end, step):
        x = get_interval(x_start, x_end, step)
        y = np.zeros(len(x))
        y[0] = y_start
        for i in range(1, len(x)):
            y[i] = y[i-1] + (self.f(x[i-1], y[i-1]) +
                             self.f(x[i], y[i-1] + self.f(x[i-1], y[i-1])*step))*step/2
        return x, y

