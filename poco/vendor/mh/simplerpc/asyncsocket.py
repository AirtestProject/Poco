from __future__ import print_function

import asyncore
import collections
import socket


LOOP_STARTED = False
MAX_MESSAGE_LENGTH = 4096


class BaseClient(asyncore.dispatcher):

    """base class for both local/remote client socket."""

    def __init__(self):
        asyncore.dispatcher.__init__(self)
        self.outbox = collections.deque()
        self.inbox = ""
        self.closed = False

    def say(self, message):
        self.outbox.append(message)

    def writable(self):
        return bool(self.outbox)

    def handle_write(self):
        if not self.outbox:
            return
        message = self.outbox.popleft()
        self.send(message)

    def handle_read(self):
        message = self.recv(MAX_MESSAGE_LENGTH)
        self.inbox += message

    def handle_close(self):
        print("Closed", self)
        self.close()
        self.closed = True

    def read_message(self, length=None):
        if length is None:
            message, self.inbox = self.inbox, ""
        else:
            message, self.inbox = self.inbox[:length], self.inbox[length:]
        return message


class RemoteClient(BaseClient):

    """Wraps a remote client socket."""

    def __init__(self, host, socket, address, cid=None):
        BaseClient.__init__(self)
        self.host = host
        self.cid = cid
        self.set_socket(socket)

    def handle_close(self):
        BaseClient.handle_close(self)
        self.host.remote_clients.pop(self.cid)


class Host(asyncore.dispatcher):

    CLIENT_ID_COUNTER = 1
    CLIENT_MAX_COUNT = 10

    def __init__(self, address=('0.0.0.0', 5001)):
        asyncore.dispatcher.__init__(self)
        self.create_socket(socket.AF_INET, socket.SOCK_STREAM)
        self.bind(address)
        self.listen(self.CLIENT_MAX_COUNT)
        print('server listening at', address)
        self.remote_clients = {}
        self.msg_queue = []

    def handle_accept(self):
        socket, addr = self.accept()  # For the remote client.
        print('Accepted client at %s', addr)
        client_id = self.__class__.CLIENT_ID_COUNTER
        self.__class__.CLIENT_ID_COUNTER += 1
        client = RemoteClient(self, socket, addr, client_id)
        self.remote_clients[client_id] = client
        print('connected clients', self.remote_clients)

    def swap_msg_queue(self):
        for client in self.remote_clients.values():
            message = client.read_message()
            self.msg_queue.append(message)

        msg_queue = self.msg_queue
        self.msg_queue = []
        return msg_queue

    def broadcast(self, message):
        print('Broadcasting message: %s' % len(message))
        for remote_client in self.remote_clients.values():
            remote_client.say(message)

    def say(self, client_id, message):
        self.remote_clients[client_id].say(message)

    def close_client(self, client_id):
        print('Close client:', client_id)
        client = self.remote_clients.pop(client_id)
        client.close()


class Client(BaseClient):

    def __init__(self, host_address, name=""):
        BaseClient.__init__(self)
        self.create_socket(socket.AF_INET, socket.SOCK_STREAM)
        self.name = name
        print('Connecting to host at %s', host_address)
        self.connect(host_address)

    def handle_connect(self):
        print(self.name + " is connected")


def start_thread(target, *args, **kwargs):
    import threading
    t = threading.Thread(target=target, args=args, kwargs=kwargs)
    t.daemon = True
    t.start()


def init_loop():
    if LOOP_STARTED:
        print("LOOP_STARTED")
    else:
        start_thread(asyncore.loop, timeout=0.001)


if __name__ == '__main__':
    h = Host()
    asyncore.loop()
