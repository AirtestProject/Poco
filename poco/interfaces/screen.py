# coding=utf-8
__author__ = 'lxn3032'


class ScreenInterface(object):
    def snapshot(self, width):
        raise NotImplementedError

    def get_screen_size(self):
        raise NotImplementedError
