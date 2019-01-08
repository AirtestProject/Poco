# -*- coding: utf-8 -*-
# @Author: gzliuxin
# @Email:  gzliuxin@corp.netease.com
# @Date:   2017-07-12 16:56:14

import json
import time
import traceback
import uuid

from .jsonrpc import JSONRPCResponseManager, dispatcher
from .jsonrpc.jsonrpc2 import JSONRPC20Response
from .jsonrpc.exceptions import JSONRPCServerError
from .jsonrpc import six


DEBUG = False
BACKEND_UPDATE = False


class Callback(object):
    """Callback Proxy"""

    WAITING, RESULT, ERROR, CANCELED = 0, 1, 2, 3

    def __init__(self, rid, agent=None):
        super(Callback, self).__init__()
        self.rid = rid
        self.agent = agent
        self.result_callback = None
        self.error_callback = None
        self.status = self.WAITING
        self.result = None
        self.error = None

    def on_result(self, func):
        if not callable(func):
            raise RuntimeError("%s should be callbale" % func)
        self.result_callback = func

    def on_error(self, func):
        if not callable(func):
            raise RuntimeError("%s should be callbale" % func)
        self.error_callback = func

    def rpc_result(self, data):
        self.result = data
        if callable(self.result_callback):
            # callback function, set result as function return value
            try:
                self.result_callback(data)
            except Exception:
                traceback.print_exc()
        self.status = self.RESULT

    def rpc_error(self, data):
        self.error = data
        if callable(self.error_callback):
            try:
                self.error_callback(data)
            except Exception:
                traceback.print_exc()
        self.status = self.ERROR

    def cancel(self):
        self.result_callback = None
        self.error_callback = None
        self.status = self.CANCELED

    def wait(self, timeout=None):
        start_time = time.time()
        while True:
            if not BACKEND_UPDATE:
                self.agent.update()
            if self.status == self.WAITING:
                time.sleep(0.005)
                if timeout and time.time() - start_time > timeout:
                    raise RpcTimeoutError(self)
            else:
                break
        return self.result, self.error

    def __str__(self):
        conn = self.agent.get_connection()
        return '{} (rid={}) (connection="{}")'.format(repr(self), self.rid, conn)


class AsyncResponse(object):

    def __init__(self):
        self.conn = None
        self.rid = None

    def setup(self, conn, rid):
        self.conn = conn
        self.rid = rid

    def result(self, result):
        ret = JSONRPC20Response(_id=self.rid, result=result)
        if DEBUG:
            print("-->", ret)

        self.conn.send(ret.json)

    def error(self, error):
        assert isinstance(error, Exception), "%s must be Exception" % error
        data = {
            "type": error.__class__.__name__,
            "args": error.args,
            "message": str(error),
        }
        ret = JSONRPC20Response( _id=self.rid, error=JSONRPCServerError(data=data)._data)
        if DEBUG:
            print("-->", ret)
        self.conn.send(ret.json)


class RpcAgent(object):
    """docstring for RpcAgent"""

    REQUEST = 0
    RESPONSE = 1

    def __init__(self):
        super(RpcAgent, self).__init__()
        self._id = six.text_type(uuid.uuid4())
        self._callbacks = {}

    def call(self, *args, **kwargs):
        raise NotImplementedError

    def get_connection(self):
        raise NotImplementedError

    def format_request(self, func, *args, **kwargs):
        rid = self._id
        payload = {
            "method": func,
            "params": args or kwargs or [],
            "jsonrpc": "2.0",
            "id": rid,
        }
        self._id = six.text_type(uuid.uuid4())  # prepare next request id
        # send rpc
        req = json.dumps(payload)
        if DEBUG:
            print("-->", req)
        # init cb
        cb = Callback(rid, self)
        self._callbacks[rid] = cb
        return req, cb

    def handle_request(self, req):
        res = JSONRPCResponseManager.handle(req, dispatcher).data
        return res

    def handle_message(self, msg, conn):
        if isinstance(msg, six.binary_type):
            # py3里 json 只接受str类型，py2没有这个限制
            msg = msg.decode('utf-8')
        data = json.loads(msg)
        if DEBUG:
            print("<--", data)
        if "method" in data:
            # rpc request
            message_type = self.REQUEST
            result = self.handle_request(msg)

            if isinstance(result.get("result"), AsyncResponse):
                result["result"].setup(conn, result["id"])
            else:
                # if DEBUG:
                #     print("-->", result)
                conn.send(json.dumps(result))

        else:
            # rpc response
            message_type = self.RESPONSE
            result = None
            # handle callback
            callback = self._callbacks.pop(data["id"])
            if "result" in data:
                callback.rpc_result(data["result"])
            elif "error" in data:
                callback.rpc_error(data["error"])
            else:
                pass
        return message_type, result

    def update(self):
        raise NotImplementedError

    def run(self):
        def _run():
            while True:
                self.update()
                time.sleep(0.002)
        if BACKEND_UPDATE:
            from threading import Thread
            t = Thread(target=_run, name="update")
            t.daemon = True
            t.start()
        else:
            _run()

    def console_run(self, local_dict=None):
        global BACKEND_UPDATE
        BACKEND_UPDATE = True
        self.run()
        from code import InteractiveInterpreter
        i = InteractiveInterpreter(local_dict)
        while True:
            prompt = ">>>"
            try:
                line = input(prompt)
            except EOFError:
                print("closing..")
                return
            i.runcode(line)


class RpcTimeoutError(Exception):
    pass


class RpcConnectionError(Exception):
    pass
