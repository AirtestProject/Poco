# coding=utf-8


class IConnection(object):

    def send(self, msg):
        raise NotImplementedError

    def recv(self):
        raise NotImplementedError


class IClient(IConnection):
    def __init__(self):
        super(IClient, self).__init__()
        self.connect_cb = None  # callable()
        self.close_cb = None  # callable()

    def on_connect(self):
        """
        this function must be called on_connect
        """
        if callable(self.connect_cb):
            self.connect_cb()

    def on_close(self):
        """
        this function must be called on_close
        """
        if callable(self.close_cb):
            self.close_cb()

    def connect(self):
        raise NotImplementedError

    def close(self):
        raise NotImplementedError
