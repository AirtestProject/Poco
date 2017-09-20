import time
import websocket
from threading import Thread
from ..interfaces import IClient


DEFAULT_ADDR = "ws://localhost:5003"


class WebSocketClient(IClient):

    def __init__(self, addr):
        super(WebSocketClient, self).__init__()
        self.client = WebSocketHandler(addr)

    def connect(self):
        print("connecting server..")
        t = Thread(target=self.client.ws.run_forever)
        t.daemon = True
        t.start()
        for i in range(10):
            print("waiting for handshake")
            if self.client._connected:
                return True
            if self.client._error:
                raise RuntimeError(self.client._error)
            time.sleep(0.5)
        raise RuntimeError("connecting timeout")

    def send(self, msg):
        if isinstance(msg, str):
            msg = msg.decode("utf-8")
        self.client.ws.send(msg)

    def recv(self):
        messages = self.client.swap_message()
        return messages



class WebSocketHandler(object):

    def __init__(self, addr=DEFAULT_ADDR):
        super(WebSocketHandler, self).__init__()
        self.addr = addr
        self.ws = self.init_ws()
        self._inbox = []
        self._connected = False
        self._error = False

    def init_ws(self):
        # ws.enableTrace(True)
        ws = websocket.WebSocketApp(self.addr,
                                    on_message=self.on_message,
                                    on_error=self.on_error,
                                    on_close=self.on_close)
        ws.on_open = self.on_open
        return ws

    def on_message(self, ws, message):
        # print("on message", message)
        self._inbox.append(message)

    def on_error(self, ws, error):
        print("on error", error)
        self._error = error

    def on_close(self, ws):
        print("on close")
        self._connected = False

    def on_open(self, ws):
        print('on open')
        self._connected = True

    def swap_message(self):
        msg, self._inbox = self._inbox, []
        return msg

