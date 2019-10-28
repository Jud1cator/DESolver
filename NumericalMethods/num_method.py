from abc import ABC, abstractmethod

import numpy as np


class NumericalMethod(ABC):

    @abstractmethod
    def __init__(self, f):
        self.f = f

    @abstractmethod
    def solve(self, x_start, y_start, x_end, step):
        pass


def get_interval(x_start, x_end, step):
    return np.arange(x_start, x_end, step)
