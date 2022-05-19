# coding=utf-8
import websocket
from threading import Thread
from ..interfaces import IClient
from poco.utils import six


DEFAULT_ADDR = "ws://localhost:5003"


class WebSocketClient(IClient):

    def __init__(self, addr=DEFAULT_ADDR):
        super(WebSocketClient, self).__init__()
        self.addr = addr
        self._inbox = []
        self._ws = None
        self._ws_thread = None

    def __str__(self):
        return self.addr
    __repr__ = __str__

    def connect(self):
        if self._ws_thread:
            self.close()
        print("connecting server..")
        self._init_ws_thread()

    def send(self, msg):
        if not isinstance(msg, six.text_type):
            msg = msg.decode("utf-8")
        self._ws.send(msg)

    def recv(self):
        msgs, self._inbox = self._inbox, []
        return msgs

    def close(self):
        print("closing connection..")
        self._ws.close()
        self._ws_thread = None

    def _init_ws_thread(self):
        self._ws = self._init_ws()
        t = Thread(target=self._ws.run_forever)
        t.daemon = True
        t.start()
        self._ws_thread = t

    def _init_ws(self):
        ws = websocket.WebSocketApp(self.addr,
                                    on_open=self._on_ws_open,
                                    on_message=self._on_ws_message,
                                    on_error=self._on_ws_error,
                                    on_close=self._on_ws_close)
        # ws.enableTrace(True)
        return ws

    def _on_ws_message(self, ws, message):
        self._inbox.append(message)

    def _on_ws_error(self, ws, error):
        print("on error", error)
        self.on_close()

    def _on_ws_close(self, ws, *args, **kwargs):
        print("on close")
        self.on_close()

    def _on_ws_open(self, ws):
        print('on open')
        self.on_connect()
