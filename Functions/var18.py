import numpy as np
from Functions.ivp import IVP


class Var18(IVP):
    def __init__(self, x0, y0, X, h):
        super().__init__(x0, y0, X, h)
        self.pdscnt = -x0 / (1 / y0 - 1)
        self.label = 'Exact'

    def first_der(self):
        def f(x, y): return (y**2 - y) / x
        return f

    def solution(self):
        x = self.get_interval()
        y = 1 / (1 + (1 / self.y0 - 1) / self.x0 * x)
        return x, y

    def get_interval(self):
        if self.x0 <= self.pdscnt <= self.X:
            return np.arange(self.x0, self.pdscnt, self.h)
        return np.arange(self.x0, self.X, self.h)
