# coding=utf-8

__author__ = 'lxn3032'
__all__ = ['IScreen']


class IScreen(object):
    def getPortSize(self):
        raise NotImplementedError

    def getScreen(self, width=720):
        # promisable
        raise NotImplementedError
