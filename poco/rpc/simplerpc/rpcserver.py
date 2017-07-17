# encoding=utf-8
from asyncsocket import Host, init_loop
from simplerpc import RpcBaseClient
from protocol import SimpleProtocolFilter


class RpcServer(RpcBaseClient):
    """docstring for RpcServer"""
    def __init__(self):
        super(RpcServer, self).__init__()
        self.host = Host()
        self.prot = SimpleProtocolFilter()
        init_loop()

    def update(self):
        for client in self.host.remote_clients.values():
            message = client.read_message()
            if not message:
                continue
            for msg in self.prot.input(message):
                message_type, result = self.handle_message(msg)
                if message_type == self.REQUEST:
                    client.say(self.prot.pack(result))

    def call(self, cid, func, *args, **kwargs):
        req, cb = self.format_request(func, *args, **kwargs)
        msg = self.prot.pack(req)
        self.host.say(cid, msg)
        return cb


if __name__ == '__main__':
    s = RpcServer()
    # s.run()
    s.console_run({"s": s})
