from abc import ABC, abstractmethod
import numpy as np


class NumericalMethod(ABC):

    @abstractmethod
    def __init__(self, f):
        self.f = f
        self.label = ''

    @abstractmethod
    def solution(self):
        pass

