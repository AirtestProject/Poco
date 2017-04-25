# coding=utf-8
__author__ = 'lxn3032'


import time
import functools

from hunter_cli.rpc.exceptions import HunterRpcRemoteException, HunterRpcTimeoutException


QueryAttributeNames = (
    'type', 'text', 'enable', 'visable', 'touchenable',
)


def build_query(name, **attrs):
    for attr_name in attrs.keys():
        if attr_name not in QueryAttributeNames:
            raise Exception('Unsupported Attribute name for query  !!!')
    query = []
    if name:
        attrs['name'] = name
    for attr_name, attr_val in attrs.items():
        query.append(('attr=', (attr_name, attr_val)))
    return 'and', tuple(query)


def retries_when(exctype, count=3):
    def wrapper(func):
        @functools.wraps(func)
        def wrapped(*args, **kwargs):
            ex = None
            for i in range(count):
                try:
                    return func(*args, **kwargs)
                except exctype as e:
                    ex = e
            raise ex
        return wrapped
    return wrapper


class UIObjectProxy(object):
    def __init__(self, poco, name=None, **attrs):
        self.query = build_query(name, **attrs)
        self.poco = poco

    def child(self, name=None, **attrs):
        child_query = build_query(name, **attrs)
        query = ('/', (self.query, child_query))
        obj = UIObjectProxy(self.poco)
        obj.query = query
        return obj

    def offspring(self, name=None, **attrs):
        child_query = build_query(name, **attrs)
        query = ('>', (self.query, child_query))
        obj = UIObjectProxy(self.poco)
        obj.query = query
        return obj

    def __getitem__(self, item):
        obj = UIObjectProxy(self.poco)
        obj.query = ('index', (self.query, item))
        return obj

    @retries_when(HunterRpcTimeoutException)
    def __len__(self):
        return self.poco.selector.selectAndGetAttribute(self.query, 'length')

    @retries_when(HunterRpcTimeoutException)
    def click(self):
        pos = self.poco.selector.selectAndGetAttribute(self.query, 'centerPositionInScreen')
        self.poco.touch(pos)
        self.poco.wait_stable()

    def wait_for_appearance(self, timeout=120):
        start = time.time()
        while not self.exists():
            self.poco.wait_for_polling_interval()
            if time.time() - start > timeout:
                raise RuntimeError('Timeout at waiting for {} to appear'.format(repr(self.query)))

    def wait_for_disappearance(self, timeout=120):
        start = time.time()
        while self.exists():
            self.poco.wait_for_polling_interval()
            if time.time() - start > timeout:
                raise RuntimeError('Timeout at waiting for {} to disappear'.format(repr(self.query)))

    @retries_when(HunterRpcTimeoutException)
    def attr(self, name):
        return self.poco.selector.selectAndGetAttribute(self.query, name)

    def exists(self):
        try:
            return self.attr('visible')
        except HunterRpcRemoteException:
            return False

    def visible(self):
        return self.attr('visible')

    def enabled(self):
        return self.attr('enable')

    def touchable(self):
        return self.attr('touchenable')

    def get_text(self):
        return self.attr('text')

    def get_name(self):
        return self.attr('name')

    def get_size(self):
        return self.attr('size')
