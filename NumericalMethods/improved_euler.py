import numpy as np
from NumericalMethods.num_method import NumericalMethod


class ImprovedEuler(NumericalMethod):

    def __init__(self, f):
        super().__init__(f)
        self.label = 'Improved Euler'

    def solution(self):
        x = self.f.get_interval()
        y = np.zeros(len(x))
        y[0] = self.f.y0
        f = self.f.first_der()
        step = self.f.h
        for i in range(1, len(x)):
            y[i] = y[i-1] + (f(x[i-1], y[i-1]) +
                             f(x[i], y[i-1] + f(x[i-1], y[i-1])*step))*step/2
        return x, y
