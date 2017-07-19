# coding=utf-8
__author__ = 'lxn3032'


class InputInterface(object):
    def click(self, pos):
        raise NotImplementedError

    def swipe(self, p1, p2=None, direction=None, duration=1):
        raise NotImplementedError

    def long_click(self, pos, duration=2):
        raise NotImplementedError

    def get_input_panel_size(self):
        raise NotImplementedError
