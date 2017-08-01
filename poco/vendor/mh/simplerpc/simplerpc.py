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


@dispatcher.add_method
def delayecho(*args):
    r = DelayResult()
    raise
    from threading import Thread

    def func(r):
        time.sleep(5)
        r.set_result(args)

    Thread(target=func, args=(r,)).start()
    return r


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

    def make_error(self, data):
        msg = "rid:%s error:%s" % (self.rid, data)
        print(msg)

    def cancel(self):
        self.func = None

    def wait(self):
        while True:
            # print(self.called)
            if not self.called:
                time.sleep(0.1)
            else:
                return (self.result, self.error)


class DelayResult(object):
    """docstring for DelayResult"""
    def __init__(self):
        super(DelayResult, self).__init__()
        self.finished = False
        self._result = None

    def get_result(self):
        if not self.finished:
            raise RuntimeError("Delay Result not Ready")
        return self._result

    def set_result(self, ret):
        self.finished = True
        self._result = ret


class RpcBaseClient(object):
    """docstring for RpcClient"""

    REQUEST = 0
    RESPONSE = 1
    REQUEST_DELAYRET = 2
    DEBUG = True

    def __init__(self):
        super(RpcBaseClient, self).__init__()
        self._id = 0
        self._callbacks = {}
        self._delayresults = {}

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
        res = JSONRPCResponseManager.handle(req, dispatcher).data
        # print("handle_request", req, res)
        return res

    def handle_message(self, msg):
        data = json.loads(msg)
        if self.DEBUG:
            print("<--", data)
        if "method" in data:
            # rpc request
            message_type = self.REQUEST
            result = self.handle_request(msg)

            if isinstance(result["result"], DelayResult):
                self._delayresults[data["id"]] = result
                message_type = self.REQUEST_DELAYRET

        else:
            # rpc response
            message_type = self.RESPONSE
            callback = self._callbacks.pop(data["id"])
            if "result" in data:
                callback.call(data["result"])
                result = (callback.result, callback.error)
            elif "error" in data:
                callback.make_error(data["error"])
                result = None
            else:
                result = None
        return message_type, result

    def handle_delay_result(self):
        # 轮询有点挫，后面优化
        for rid, res in self._delayresults.items():
            delay_result = res["result"]
            try:
                result = delay_result.get_result()
            except RuntimeError:
                continue
            self._delayresults.pop(rid)
            res["result"] = result
            yield res

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
