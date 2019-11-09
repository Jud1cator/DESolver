import numpy as np
from NumericalMethods.num_method import NumericalMethod


class RungeKutta(NumericalMethod):

    def __init__(self, func):
        super().__init__(func)
        self.label = 'Runge-Kutta'

    def solution(self):
        x = self.f.get_interval()
        y = np.zeros(len(x))
        y[0] = self.f.y0
        f = self.f.first_der()
        step = self.f.h
        for i in range(1, len(x)):
            k1 = f(x[i-1], y[i-1])
            k2 = f(x[i-1]+step/2, y[i-1]+k1*step/2)
            k3 = f(x[i-1]+step/2, y[i-1]+k2*step/2)
            k4 = f(x[i-1]+step, y[i-1]+k3*step)
            y[i] = y[i-1] + (k1+2*k2+2*k3+k4)*step/6
        return x, y
