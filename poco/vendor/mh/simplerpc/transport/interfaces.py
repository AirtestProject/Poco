class IConnection(object):

    def send(self, msg):
        raise NotImplementedError

    def recv(self):
        raise NotImplementedError


class IClient(IConnection):

    def connect(self):
        raise NotImplementedError


class IServer(object):

    def start(self):
        raise NotImplementedError

    def on_connected(self):
        raise NotImplementedError

    def on_disconnected(self):
        raise NotImplementedError

    def connections(self):
        "return {cid: Connection}"
        raise NotImplementedError

    def broadcast(self, msg):
        for conn in self.connections().values():
            conn.send(msg)
