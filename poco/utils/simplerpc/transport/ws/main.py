import time
import websocket
from threading import Thread
from ..interfaces import IClient


DEFAULT_ADDR = "ws://localhost:5003"


class WebSocketClient(IClient):

    def __init__(self, addr=DEFAULT_ADDR):
        super(WebSocketClient, self).__init__()
        self.addr = addr
        self._ws = self._init_ws()
        self._inbox = []

    def connect(self):
        print("connecting server..")
        t = Thread(target=self._ws.run_forever)
        t.daemon = True
        t.start()
        # for i in range(10):
        #     print("waiting for handshake")
        #     if self._connected:
        #         return True
        #     if self._error:
        #         raise RuntimeError(self.client._error)
        #     time.sleep(0.5)
        # raise RuntimeError("connecting timeout")

    def send(self, msg):
        if isinstance(msg, str):
            msg = msg.decode("utf-8")
        self._ws.send(msg)

    def recv(self):
        msgs, self._inbox = self._inbox, []
        return msgs

    def _init_ws(self):
        # ws.enableTrace(True)
        ws = websocket.WebSocketApp(self.addr,
                                    on_message=self._on_ws_message,
                                    on_error=self._on_ws_error,
                                    on_close=self._on_ws_close)
        ws.on_open = self._on_ws_open
        return ws

    def _on_ws_message(self, ws, message):
        # print("on message", message)
        self._inbox.append(message)

    def _on_ws_error(self, ws, error):
        print("on error", error)

    def _on_ws_close(self, ws):
        print("on close")
        self.on_close()

    def _on_ws_open(self, ws):
        print('on open')
        self.on_connect()

