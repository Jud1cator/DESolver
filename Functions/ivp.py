from abc import ABC, abstractmethod


class IVP(ABC):
    @abstractmethod
    def __init__(self, x0, y0, X, h):
        self.x0 = x0
        self.y0 = y0
        self.X = X
        self.h = h
        self.label = 'Exact'
        self.pdscnt = None

    @abstractmethod
    def first_der(self):
        pass

    @abstractmethod
    def solution(self):
        pass

    @abstractmethod
    def get_interval(self):
        pass
