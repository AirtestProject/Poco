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


class IServer(object):

    def __init__(self):
        super(IServer, self).__init__()
        self.client_connect_cb = None  # callable(conn)
        self.client_close_cb = None  # callable(conn)

    def on_client_connect(self, conn):
        """
        this function must be called on_client_connect
        """
        if callable(self.client_connect_cb):
            self.client_connect_cb(conn)

    def on_client_close(self, conn):
        """
        this function must be called on_client_close
        """
        if callable(self.client_close_cb):
            self.client_close_cb(conn)

    @property
    def connections(self):
        # return {cid: IConnection}
        raise NotImplementedError

    def start(self):
        raise NotImplementedError

    def broadcast(self, msg):
        for conn in self.connections.values():
            conn.send(msg)
