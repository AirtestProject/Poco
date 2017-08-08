# -*- coding: utf-8 -*-
# @Author: gzliuxin
# @Email:  gzliuxin@corp.netease.com
# @Date:   2017-07-14 19:47:51
from SimpleWebSocketServer import SimpleWebSocketServer, WebSocket
from poco.interfaces.rpc import RpcInterface
from poco.vendor.mh.simplerpc.simplerpc import Connection
from poco.vendor.mh.simplerpc.rpcclient import RpcClient
from poco.vendor.mh.mh_rpc import sync_wrapper, MhRpc
from airtest.core.main import touch, swipe, snapshot
from airtest.cli.runner import device as current_device
from poco.exceptions import InvalidOperationException
from poco import Poco
from threading import Thread
import time

DEFAULT_ADDR = ('', 5001)


class CocosJsPoco(Poco):
    """docstring for CocosJsPoco"""
    def __init__(self, addr=DEFAULT_ADDR):
        self._rpc_client = SocketIORpc(addr)
        super(CocosJsPoco, self).__init__(self._rpc_client, action_interval=0.01)

    def _get_touch_resolution(self):
        size = current_device().size
        w, h = size["width"], size["height"]
        if size["orientation"] in (1, 3):
            return h, w
        else:
            return w, h

    def click(self, pos):
        if not (0 <= pos[0] <= 1) or not (0 <= pos[1] <= 1):
            raise InvalidOperationException('Click position out of screen. {}'.format(pos))

        # Note: 临时使用，记得删掉
        self.snapshot(str(self._last_proxy))

        panel_size = self._get_touch_resolution()
        pos = [pos[0] * panel_size[0], pos[1] * panel_size[1]]
        touch(pos)

    def swipe(self, p1, p2=None, direction=None, duration=1):
        if not (0 <= p1[0] <= 1) or not (0 <= p1[1] <= 1):
            raise InvalidOperationException('Swipe origin out of screen. {}'.format(p1))
        panel_size = self._get_touch_resolution()
        p1 = [p1[0] * panel_size[0], p1[1] * panel_size[1]]
        if p2:
            p2 = [p2[0] * panel_size[0], p2[1] * panel_size[1]]
        steps = int(duration * 40) + 1
        if not direction:
            swipe(p1, p2, duration=duration, steps=steps)
        else:
            swipe(p1, vector=direction, duration=duration, steps=steps)

    def snapshot(self, width):
        # width as massage
        width = width.decode('utf-8')
        if not width.endswith('.png'):
            width += '.png'
        snapshot(msg=width)


class SimpleWS(WebSocket):

    def __init__(self, *args, **kwargs):
        super(SimpleWS, self).__init__(*args, **kwargs)
        self._inbox = []

    def handleMessage(self):
        # print('ws handleMessage', self.data)
        self._inbox.append(self.data)

    def handleConnected(self):
        print(self.address, 'connected')

    def handleClose(self):
        print(self.address, 'closed')

    def swapMessage(self):
        msg, self._inbox = self._inbox, []
        return msg


class SocketIORpc(MhRpc):
    def __init__(self, addr=DEFAULT_ADDR):
        self.conn = SocketIOConnection(addr)
        self.c = RpcClient(self.conn)
        self.c.DEBUG = False
        self.c.run(backend=True)

    @sync_wrapper
    def dump(self):
        return self.c.call("dump")

    def close(self):
        """关闭server."""
        self.conn.server.close()


class SocketIOConnection(Connection):
    def __init__(self, addr):
        self.server = self.init_server(addr[0], addr[1])
        self.client_index = 0

    @staticmethod
    def init_server(host, port):
        server = SimpleWebSocketServer(host, port, SimpleWS)
        t = Thread(target=server.serveforever)
        t.daemon = True
        t.start()
        return server

    @property
    def client(self):
        try:
            c = self.server.connections.values()[self.client_index]
        except IndexError:
            raise RuntimeError("client %s not connected" % self.client_index)
        return c

    def connect(self):
        for i in range(10):
            if self.server.connections:
                return True
            time.sleep(2)
            print("wait for client")
        raise RuntimeError("no client connected")

    def send(self, msg):
        if isinstance(msg, str):
            msg = msg.decode("utf-8")
        self.client.sendMessage(msg)

    def recv(self):
        messages = self.client.swapMessage()
        return messages
