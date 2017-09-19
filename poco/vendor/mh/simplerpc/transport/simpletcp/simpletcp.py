# -*- coding: utf-8 -*-
# @Author: gzliuxin
# @Email:  gzliuxin@corp.netease.com
# @Date:   2017-07-12 17:58:23
import socket
import errno


class SafeSocket(object):
    """safe and exact recv & send"""
    def __init__(self, sock=None, address=None):
        self.address = address
        if sock is None:
            self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        else:
            self.sock = sock
        self.buf = ""

    def connect(self, address=None):
        self.address = address or self.address
        self.sock.connect(self.address)

    def send(self, msg):
        totalsent = 0
        while totalsent < len(msg):
            sent = self.sock.send(msg[totalsent:])
            if sent == 0:
                raise socket.error("socket connection broken")
            totalsent += sent

    def recv(self, size):
        while len(self.buf) < size:
            trunk = self.sock.recv(min(size - len(self.buf), 4096))
            if trunk == "":
                raise socket.error("socket connection broken")
            self.buf += trunk
        ret, self.buf = self.buf[:size], self.buf[size:]
        return ret

    def recv_with_timeout(self, size, timeout=2):
        self.sock.settimeout(timeout)
        try:
            ret = self.recv(size)
        except socket.timeout:
            ret, self.buf = self.buf, ""
        except socket.error, e:
            #  10035 no data when nonblocking
            # if e.args[0] in [35, 10035]:  # errno.EWOULDBLOCK: 尼玛errno似乎不一致
            if e.args[0] == errno.EWOULDBLOCK:
                ret, self.buf = self.buf, ""
            #  10053 connection abort by client
            #  10054 connection reset by peer
            elif e.args[0] in [10053, 10054]:  # errno.ECONNABORTED:
                raise e
            else:
                raise e
        finally:
            self.sock.settimeout(None)
        return ret

    def recv_nonblocking(self, size=4096):
        self.sock.settimeout(0)
        ret = self.recv_with_timeout(size, 0)
        return ret

    def close(self):
        self.sock.close()
