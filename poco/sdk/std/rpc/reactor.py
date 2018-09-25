# coding=utf-8
import traceback
import uuid

from poco.utils import six


class NoSuchMethod(Exception):
    def __init__(self, name, available_methods):
        msg = 'No such method "{}". Available methods {}'.format(name, available_methods)
        super(NoSuchMethod, self).__init__(msg)


class StdRpcReactor(object):
    def __init__(self):
        super(StdRpcReactor, self).__init__()
        self.slots = {}  # method name -> method
        self.pending_response = {}  # rid -> result

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
                           .format(six.text_type(e), traceback.format_exc())
            }

        return ret

    def handle_response(self, res):
        id = res['id']
        self.pending_response[id] = res

    def build_request(self, method, *args, **kwargs):
        rid = six.text_type(uuid.uuid4())
        ret = {
            'id': rid,
            'jsonrpc': '2.0',
            'method': method,
            'params': args or kwargs or [],
        }
        self.pending_response[rid] = None
        return ret

    def get_result(self, rid):
        return self.pending_response.get(rid)
