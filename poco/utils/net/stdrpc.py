# coding=utf-8

"""
python语言的StdPoco用的rpc协议最简化版
目的：此版本可以直接翻译到其他语言上，避免引入python第三方库
"""

import errno
import json
import select
import socket
import struct
import traceback
import time

from poco.utils import six


DEFAULT_ADDR = ('0.0.0.0', 15004)
HEADER_SIZE = 4
RX_SIZE = 65536


class SimpleProtocolFilter(object):
    """ 简单协议过滤器
        协议按照 [有效数据字节数][有效数据] 这种协议包的格式进行打包和解包
        [有效数据字节数]长度HEADER_SIZE字节
        [有效数据]长度有效数据字节数字节
        本类按照这种方式，顺序从数据流中取出数据进行拼接，一旦接收完一个完整的协议包，就会将协议包返回
        [有效数据]字段接收到后会按照utf-8进行解码，因为在传输过程中是用utf-8进行编码的
        所有编解码的操作在该类中完成
    """

    def __init__(self):
        super(SimpleProtocolFilter, self).__init__()
        self.buf = b''

    def input(self, data):
        """ 小数据片段拼接成完整数据包
            如果内容足够则yield数据包
        """
        self.buf += data
        while len(self.buf) > HEADER_SIZE:
            data_len = struct.unpack('i', self.buf[0:HEADER_SIZE])[0]
            if len(self.buf) >= data_len + HEADER_SIZE:
                content = self.buf[HEADER_SIZE:data_len + HEADER_SIZE]
                self.buf = self.buf[data_len + HEADER_SIZE:]
                yield content
            else:
                break

    @staticmethod
    def pack(content):
        """ content should be str
        """
        if isinstance(content, six.text_type):
            content = content.encode("utf-8")
        return struct.pack('i', len(content)) + content

    @staticmethod
    def unpack(data):
        """ return length, content
        """
        length = struct.unpack('i', data[0:HEADER_SIZE])
        return length[0], data[HEADER_SIZE:]


class ClientException(Exception):
    pass


class ClientConnection(object):
    def __init__(self, sock, RX_SIZE=65536):
        super(ClientConnection, self).__init__()
        self.sock = sock
        self.p = SimpleProtocolFilter()
        self.RX_SIZE = RX_SIZE

    def recv(self):
        rxdata = ''
        try:
            rxdata = self.sock.recv(self.RX_SIZE)
        except socket.error as e:
            if e.errno in (errno.ECONNRESET, ):
                raise ClientException

        if not rxdata:
            try:
                self.sock.close()
            except socket.error:
                pass
            raise ClientException
        else:
            for packet in self.p.input(rxdata):
                yield packet

    def send(self, packet):
        data = self.p.pack(packet)
        self.sock.sendall(data)


class StdRpcServer(object):
    def __init__(self, addr=DEFAULT_ADDR):
        super(StdRpcServer, self).__init__()
        self.addr = addr
        self.s = socket.socket()
        self.s.bind(addr)
        self.s.listen(1)
        self.clients = {}  # socket -> True
        self.p = SimpleProtocolFilter()

    def serve_forever(self):
        print('[StdRpcServer] Server loop started. Listened on {}'.format(self.addr))
        while True:
            try:
                self.update()
            except:
                traceback.print_exc()

    def update(self, timeout=None):
        r, _, _ = select.select([self.s] + self.clients.keys(), [], [], timeout)
        for c in r:
            if c is self.s:
                sock, addr = self.s.accept()
                self.clients[sock] = ClientConnection(sock)
                print('accept from: {}'.format(addr))
            else:
                client = self.clients.get(c)
                if not client:
                    continue

                try:
                    for packet in client.recv():
                        try:
                            self.on_received(client, packet)
                        except:
                            traceback.print_exc()
                except ClientException:
                    self.clients.pop(c, None)

    def on_received(self, client, packet):
        pass


class NoSuchMethod(Exception):
    def __init__(self, name, available_methods):
        msg = 'No such method "{}". Available methods {}'.format(name, available_methods)
        super(NoSuchMethod, self).__init__(msg)


class RpcDispatcher(StdRpcServer):
    def __init__(self, addr=DEFAULT_ADDR):
        super(RpcDispatcher, self).__init__(addr)
        self.slots = {}  # method name -> method

    def register(self, name, method):
        if not callable(method):
            raise ValueError('Argument `method` should be a callable object. Got {}'.format(repr(method)))
        if name in self.slots:
            raise ValueError('"{}" already registered. {}'.format(name, repr(self.slots[name])))

        self.slots[name] = method

    def dispatch(self, name, *args, **kwargs):
        method = self.slots.get(name)
        if not method:
            raise NoSuchMethod(name, self.slots.keys())

        return method(*args, **kwargs)

    def handle_request(self, req):
        req = json.loads(req)
        ret = {
            'id': req['id'],
            'jsonrpc': req['jsonrpc'],
        }

        method = req['method']
        params = req['params']
        try:
            result = self.dispatch(method, *params)
            ret['result'] = result
        except Exception as e:
            ret['error'] = {
                'message': '{}\n\n|--- REMOTE TRACEBACK ---|\n{}|--- REMOTE TRACEBACK END ---|'
                           .format(e.message, traceback.format_exc())
            }

        return ret

    def on_received(self, client, packet):
        try:
            ret = self.handle_request(packet)
            sret = json.dumps(ret)
            client.send(sret)
        except:
            traceback.print_exc()


if __name__ == '__main__':
    def Dump(xxxonly):
        print('this is dump')
        return {}

    def GetSDKVersion():
        return '0.0.1'

    dispatcher = RpcDispatcher()
    dispatcher.register('D0ump', Dump)
    dispatcher.register('GetSDKVersion', GetSDKVersion)
    dispatcher.serve_forever()
