# coding=utf-8

import math
from poco.utils.track import MotionTrack


def make_pinching(direction, center, size, percent, dead_zone, duration):
    w, h = size
    half_distance = percent / 2
    dead_zone_distance = dead_zone / 2
    pa0 = center
    pb0 = list(pa0)
    pa1 = list(pa0)
    pb1 = list(pa0)
    if direction == 'in':
        pa0[0] += w * half_distance
        pa0[1] += h * half_distance
        pb0[0] -= w * half_distance
        pb0[1] -= h * half_distance
        pa1[0] += w * dead_zone_distance
        pa1[1] += h * dead_zone_distance
        pb1[0] -= w * dead_zone_distance
        pb1[1] -= h * dead_zone_distance
    else:
        pa1[0] += w * half_distance
        pa1[1] += h * half_distance
        pb1[0] -= w * half_distance
        pb1[1] -= h * half_distance
        pa0[0] += w * dead_zone_distance
        pa0[1] += h * dead_zone_distance
        pb0[0] -= w * dead_zone_distance
        pb0[1] -= h * dead_zone_distance

    speed = math.sqrt(w * h) * (percent - dead_zone) / 2 / duration
    track_a = MotionTrack([pa0, pa1], speed)
    track_b = MotionTrack([pb0, pb1], speed)

    return track_a, track_b


def make_panning():
    pass
