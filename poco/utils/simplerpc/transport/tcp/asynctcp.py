# coding=utf-8
from __future__ import print_function
import threading
import collections
import socket
try:
    from . import asyncore
except (ImportError, SyntaxError):
    import asyncore


LOOP_THREAD = None
LOOP_LOCK = threading.Lock()
MAX_MESSAGE_LENGTH = 4096


class BaseClient(asyncore.dispatcher):

    """base class for both local/remote client socket."""

    def __init__(self):
        asyncore.dispatcher.__init__(self)
        self.outbox = collections.deque()
        self.read_lock = threading.Lock()
        self.inbox = b""
        self.closed = False

    def say(self, message):
        self.outbox.append(message)

    def writable(self):
        if self.connecting:  # is it a bug in asynccore? handle_connect_event triggered only when writable is True
            return True
        return bool(self.outbox)

    def handle_write(self):
        if not self.outbox:
            return
        message = self.outbox.popleft()
        self.send(message)

    def handle_read(self):
        if not self.connected:
            return
        message = self.recv(MAX_MESSAGE_LENGTH)
        if message == b"":
            return
        with self.read_lock:
            self.inbox += message

    def handle_close(self):
        asyncore.dispatcher.handle_close(self)
        print("Closed", self)
        self.closed = True

    def read_message(self, length=None):
        with self.read_lock:
            if length is None:
                message, self.inbox = self.inbox, b""
            else:
                message, self.inbox = self.inbox[:length], self.inbox[length:]
        return message


class Client(BaseClient):

    def __init__(self, host_address, on_connect=None, on_close=None):
        BaseClient.__init__(self)
        self.addr = host_address
        self.create_socket(socket.AF_INET, socket.SOCK_STREAM)
        self.on_connect = on_connect
        self.on_close = on_close

    def connect_server(self):
        print('Connecting to host at: %s' % repr(self.addr))
        self.connect(self.addr)

    def handle_connect(self):
        # BaseClient.handle_connect(self)
        print("%s is connected" % self)
        if callable(self.on_connect):
            self.on_connect()

    def handle_close(self):
        BaseClient.handle_close(self)
        print("%s is closed" % self)
        if callable(self.on_close):
            self.on_close()

    def close_connection(self):
        with LOOP_LOCK:
            BaseClient.close(self)
        self.on_close()


class LoopThread(threading.Thread):
    def __init__(self, *args, **kwargs):
        super(LoopThread, self).__init__(*args, **kwargs)
        self._kill_event = threading.Event()

    def run(self):
        while not self._kill_event.is_set():
            with LOOP_LOCK:
                asyncore.loop(timeout=0.001, count=1)
        print("%s finished" % self)

    def kill(self):
        self._kill_event.set()


def init_loop():
    global LOOP_THREAD
    if LOOP_THREAD and LOOP_THREAD.is_alive():
        print("LOOP_THREAD ALREADY STARTED: %s" % LOOP_THREAD)
    else:
        LOOP_THREAD = LoopThread(name="asynctcp_update")
        LOOP_THREAD.daemon = True
        LOOP_THREAD.start()


def wait_exit():
    if LOOP_THREAD:
        LOOP_THREAD.kill()
        LOOP_THREAD.join(1.0)


import atexit
atexit.register(wait_exit)

