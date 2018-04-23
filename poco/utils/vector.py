# coding=utf-8
__author__ = 'lxn3032'


import math


class Vec2(object):
    def __init__(self, x=0.0, y=0.0):
        if type(x) in (list, tuple):
            self.x = x[0]
            self.y = x[1]
        else:
            self.x = x
            self.y = y

    @staticmethod
    def from_radian(rad):
        x = math.cos(rad)
        y = math.sin(rad)
        return Vec2(x, y)

    def __add__(self, other):
        return Vec2(self.x + other.x, self.y + other.y)

    def __sub__(self, other):
        return Vec2(self.x - other.x, self.y - other.y)

    def __radd__(self, other):
        return Vec2(other.x + self.x, other.y + self.y)

    def __rsub__(self, other):
        return Vec2(other.x - self.x, other.y - self.y)

    def __mul__(self, other):
        return Vec2(self.x * other, self.y * other)

    def __rmul__(self, other):
        return Vec2(self.x * other, self.y * other)

    def to_list(self):
        return [self.x, self.y]

    @classmethod
    def intersection_angle(cls, v1, v2):
        cosval = cls.dot_product(v1, v2) / (v1.length * v2.length)
        if -2 < cosval < -1:
            cosval = -1
        elif 1 < cosval < 2:
            cosval = 1
        return math.acos(cosval) * (1 if cls.cross_product(v1, v2) > 0 else -1)

    @staticmethod
    def dot_product(v1, v2):
        return v1.x * v2.x + v1.y * v2.y

    @staticmethod
    def cross_product(v1, v2):
        return v1.x * v2.y - v2.x * v1.y

    @property
    def length(self):
        return math.sqrt(self.x ** 2 + self.y ** 2)

    def unit(self):
        length = self.length
        return Vec2(self.x / length, self.y / length)

    def rotate(self, radian):
        qx = math.cos(radian) * self.x - math.sin(radian) * self.y
        qy = math.sin(radian) * self.x + math.cos(radian) * self.y
        self.x, self.y = qx, qy

    def __str__(self):
        return '({}, {})'.format(self.x, self.y)
    __repr__ = __str__
