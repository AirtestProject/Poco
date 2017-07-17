# -*- coding: utf-8 -*-
# @Author: gzliuxin
# @Email:  gzliuxin@corp.netease.com
# @Date:   2017-07-12 16:56:14
from jsonrpc import JSONRPCResponseManager, dispatcher
import json
import time
import traceback


@dispatcher.add_method
def foobar(**kwargs):
    return kwargs["foo"] + kwargs["bar"]


@dispatcher.add_method
def echo(*args):
    return args


class Callback(object):
    """Callback Proxy"""
    def __init__(self, rid):
        super(Callback, self).__init__()
        self.rid = rid
        self.func = None
        self.called = False
        self.result = None
        self.error = None

    def callback(self, func):
        if not callable(func):
            raise RuntimeError("func should be callbale", func)
        self.func = func

    def call(self, rpc_result):
        if callable(self.func):
            # callback function, set result as function return value
            try:
                self.result = self.func(rpc_result)
            except Exception:
                self.error = traceback.format_exc()
                print(self.error)
            finally:
                self.called = True
        else:
            # no callback, set result as rpc_result
            self.result = rpc_result
            self.called = True

    def cancel(self):
        self.func = None

    def wait(self):
        while True:
            # print(self.called)
            if not self.called:
                time.sleep(0.1)
            else:
                return (self.result, self.error)


class RpcBaseClient(object):
    """docstring for RpcClient"""

    REQUEST = 0
    RESPONSE = 1
    DEBUG = True

    def __init__(self):
        super(RpcBaseClient, self).__init__()
        self._id = 0
        self._callbacks = {}

    def call(self, *args, **kwargs):
        raise NotImplementedError

    def format_request(self, func, *args, **kwargs):
        rid = self._id
        payload = {
            "method": func,
            "params": args or kwargs,
            "jsonrpc": "2.0",
            "id": rid,
        }
        self._id += 1
        # send rpc
        req = json.dumps(payload)
        if self.DEBUG:
            print("-->", req)
        # init cb
        cb = Callback(rid)
        self._callbacks[rid] = cb
        return req, cb

    def handle_request(self, req):
        return JSONRPCResponseManager.handle(req, dispatcher).json

    def handle_message(self, msg):
        data = json.loads(msg)
        if self.DEBUG:
            print("<--", data)
        if "method" in data:
            # rpc request
            message_type = self.REQUEST
            result = self.handle_request(msg)
        else:
            # rpc response
            message_type = self.RESPONSE
            callback = self._callbacks.pop(data["id"])
            if "result" in data:
                callback.call(data["result"])
                result = (callback.result, callback.error)
            else:
                result = None
        return message_type, result

    def update(self):
        raise NotImplementedError

    def run(self, backend=False):
        def _run():
            while True:
                self.update()
                time.sleep(0.1)
        if backend:
            from threading import Thread
            t = Thread(target=_run, name="update")
            t.daemon = True
            t.start()
        else:
            _run()

    def console_run(self, local_dict=None):
        self.run(backend=True)
        from code import InteractiveInterpreter
        i = InteractiveInterpreter(local_dict)
        while True:
            prompt = ">>>"
            try:
                line = raw_input(prompt)
            except EOFError:
                print("closing..")
                return
            i.runcode(line)


class Connection(object):
    """docstring for Connection"""

    def connect(self):
        raise NotImplementedError

    def send(self, msg):
        raise NotImplementedError

    def recv(self):
        raise NotImplementedError
