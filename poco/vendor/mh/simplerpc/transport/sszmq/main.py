# coding=utf-8
from .SSRPC import setup_client, setup_server, init, tick, SERV_MODE_ALL_GET_MSG, ZMQHandler
from .SSRPC.SSRPC import _pack, _HEARTBEAT_DATA, _HEARTBEAT_SEC
from ..interfaces import IServer, IClient, IConnection
import time



class ServerHandler(ZMQHandler):

    def __init__(self, client_connect_cb=None, client_disconnect_cb=None):
        super(ServerHandler, self).__init__()
        self.on_client_connect = client_connect_cb
        self.on_client_disconnect = client_disconnect_cb
        self.online_clients = {}

    def on_init_finish(self, rtn):
        print("on_init_finish", rtn)

    def _on_multi_data(self, msgs):
        self._zmq_cache_msgs.extend(msgs)
        while len(self._zmq_cache_msgs) >= 2:
            cid = self._zmq_cache_msgs.pop(0)
            data = self._zmq_cache_msgs.pop(0)
            # print(cid, data)
            if cid == b"myclients_cb":  # 特殊信息
                continue

            conn = self.online_clients.get(cid)
            if not conn:
                conn = SSZmqConn(cid, self)
                self.online_clients[cid] = conn
                self.on_client_connect(cid)
            conn.lastHeartBeat = time.time()
            if data != _HEARTBEAT_DATA:
                data = self._unpack_data(data)
                conn.inbox.append(data)

    def send(self, client_id, data):
        self._zmq_socket.send_multipart([client_id, self._pack_data(data)])

    def send_heartbeat(self):
        self._zmq_socket.send_multipart([_HEARTBEAT_DATA, _pack(self._my_id)])

        for cli in list(self.online_clients):
            if time.time() - self.online_clients[cli].lastHeartBeat > _HEARTBEAT_SEC * 2:
                self.on_client_disconnect(cli)
                self.online_clients.pop(cli)


class ClientHandler(ZMQHandler):
    def __init__(self):
        super(ClientHandler, self).__init__()
        self.inbox = []

    def on_init_finish(self, rtn):
        print("on_init_finish", rtn)

    def _on_raw_data(self, data):
        data = self._unpack_data(data)
        self.inbox.append(data)

    def send(self, data):
        if hasattr(self, "_zmq_socket") and self._zmq_socket is not None:
            self._zmq_socket.send(self._pack_data(data))

    def send_heartbeat(self):
        self._zmq_socket.send(_HEARTBEAT_DATA)

    def recv(self):
        msgs, self.inbox = self.inbox, []
        return msgs


class SSZmqConn(IConnection):
    def __init__(self, cid, sh):
        self.cid = cid
        self.sh = sh
        self.inbox = []
        self.lastHeartbeat = 0

    def send(self, msg):
        self.sh.send(self.cid, msg)

    def recv(self):
        msgs, self.inbox = self.inbox, []
        return msgs


class SSZmqServer(IServer):
    def __init__(self, addr=("g68", "ff_server")):
        super(SSZmqServer, self).__init__()
        self.addr = addr
        self.sh = ServerHandler(client_connect_cb=self.on_client_connect, client_disconnect_cb=self.on_client_disconnect)

    def start(self):
        init(self.addr[0], err_handler=init_err_handler)
        setup_server(self.addr[1], self.sh, SERV_MODE_ALL_GET_MSG)

    @property
    def connections(self):
        return self.sh.online_clients


class SSZmqClient(IClient):
    def __init__(self, addr=("g68", "ff_server")):
        self.addr = addr
        self.ch = ClientHandler()

    def connect(self):
        init(self.addr[0], err_handler=init_err_handler)
        setup_client(self.addr[1], self.ch)

    def send(self, msg):
        self.ch.send(msg)

    def recv(self):
        return self.ch.recv()


def init_err_handler(code, msg):
    print("my_err_handler %d %s"%(code, msg))
