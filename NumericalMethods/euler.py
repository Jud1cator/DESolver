import numpy as np
from NumericalMethods.num_method import NumericalMethod


class Euler(NumericalMethod):

    def __init__(self, f):
        super().__init__(f)
        self.label = 'Euler'

    def solution(self):
        x = self.f.get_interval()
        y = np.zeros(len(x))
        y[0] = self.f.y0
        for i in range(1, len(x)):
            y[i] = y[i-1] + self.f.first_der()(x[i-1], y[i-1])*self.f.h
        return x, y
