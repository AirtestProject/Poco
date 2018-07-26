# coding=utf-8


class Transport(object):
    def update(self, timeout=None):
        raise NotImplementedError

    def send(self, cid, data):
        raise NotImplementedError

    def recv(self):
        raise NotImplementedError

    def connect(self, endpoint):
        raise NotImplementedError

    def disconnect(self, endpoint=None):
        raise NotImplementedError

    def bind(self, endpoint):
        raise NotImplementedError
