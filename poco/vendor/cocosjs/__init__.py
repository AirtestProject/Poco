# -*- coding: utf-8 -*-
# @Author: gzliuxin
# @Email:  gzliuxin@corp.netease.com
# @Date:   2017-07-14 19:47:51
import json
import time
import websocket
from threading import Thread

from poco import Poco
from poco.agent import PocoAgent
from poco.vendor.localui.hierarchy import LocalUIHierarchy, LocalUIDumper
from poco.vendor.airtest.screen import AirtestScreen
from poco.vendor.airtest.input import AirtestInput
from poco.vendor.mh.mh_rpc import sync_wrapper
from poco.vendor.mh.simplerpc.rpcclient import RpcClient
from poco.vendor.mh.simplerpc.simplerpc import Connection


DEFAULT_ADDR = "ws://localhost:5003"


class CocosJsPocoAgent(PocoAgent):
    def __init__(self, addr=DEFAULT_ADDR):
        # init airtest env
        from airtest.core.main import set_serialno
        from airtest.cli.runner import device as current_device
        if not current_device():
            set_serialno()
        current_device().adb.forward("tcp:5003", "tcp:5003", False)

        self.conn = SocketIOConnection(addr)
        self.c = RpcClient(self.conn)
        self.c.DEBUG = False
        self.c.run(backend=True)

        hierarchy = LocalUIHierarchy(Dumper(self.c))
        screen = AirtestScreen()
        input = AirtestInput()
        super(CocosJsPocoAgent, self).__init__(hierarchy, input, screen, None)


class Dumper(LocalUIDumper):

    def __init__(self, rpcclient):
        super(Dumper, self).__init__()
        self.rpcclient = rpcclient

    @sync_wrapper
    def dumpHierarchy(self):
        return self.rpcclient.call("dump")


class CocosJsPoco(Poco):
    """docstring for CocosJsPoco"""

    def __init__(self, addr=DEFAULT_ADDR):
        agent = CocosJsPocoAgent(addr)
        super(CocosJsPoco, self).__init__(agent, action_interval=0.01)


class SocketIOConnection(Connection):

    def __init__(self, addr):
        self.client = WebSocketClient(addr)

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
        # print(msg)
        self.client.ws.send(msg)

    def recv(self):
        messages = self.client.swap_message()
        return messages


class WebSocketClient(object):

    def __init__(self, addr=DEFAULT_ADDR):
        super(WebSocketClient, self).__init__()
        self.addr = addr
        self.ws = self.init_ws()
        self._inbox = []
        self._connected = False
        self._error = False

    def init_ws(self):
        # websocket.enableTrace(True)
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


# test code
def dump():
    from websocket import create_connection
    ws = create_connection(DEFAULT_ADDR, timeout=2)
    ws.send('{"jsonrpc": "2.0", "params": {}, "method": "dump", "id": 0}')
    print("Sent")
    print("Receiving...")
    result = ws.recv()
    print("Received '%s'" % result)
    ws.close()
    data = json.loads(result)
    return data["result"]


if __name__ == '__main__':
    # ws = WebSocketClient("ws://echo.websocket.org/")
    rpc = CocosJsPocoAgent()
    t0 = time.time()
    rpc.dumpHierarchy()
    t1 = time.time()
    print t1 - t0
    # print(dump())
