# coding=utf-8


def point_inside(p, bounds):
    return bounds[3] <= p[0] <= bounds[1] and bounds[0] <= p[1] <= bounds[2]
