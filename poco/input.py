# coding=utf-8
__author__ = 'lxn3032'


class InputInterface(object):
    def touch(self, pos):
        raise NotImplementedError

    def swipe(self, p1, p2, dur):
        raise NotImplementedError

    def long_click(self, pos, interval=2):
        raise NotImplementedError
