class IConnection(object):

    def send(self, msg):
        raise NotImplementedError

    def recv(self):
        raise NotImplementedError


class IClient(IConnection):

    def on_client_connect(self, conn):
        pass

    def on_client_disconnect(self, conn):
        pass

    def connect(self):
        raise NotImplementedError


class IServer(object):

    def __init__(self):
        super(IServer, self).__init__()
        self.client_connect_cb = None  # callable(conn)
        self.client_disconnect_cb = None  # callable(conn)

    def on_client_connect(self, conn):
        """
        this function must be called on_client_connect
        """
        if callable(self.client_connect_cb):
            self.client_connect_cb(conn)

    def on_client_disconnect(self, conn):
        """
        this function must be called on_client_disconnect
        """
        if callable(self.client_disconnect_cb):
            self.client_disconnect_cb(conn)

    @property
    def connections(self):
        # return {cid: IConnection}
        raise NotImplementedError

    def start(self):
        raise NotImplementedError

    def broadcast(self, msg):
        for conn in self.connections.values():
            conn.send(msg)
