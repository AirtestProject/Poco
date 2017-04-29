# coding=utf-8
__author__ = 'lxn3032'


import copy
import time

from hunter_cli.rpc.exceptions import HunterRpcRemoteException, HunterRpcTimeoutException
from .utils.retry import retries_when


QueryAttributeNames = (
    'type', 'text', 'enable', 'visable', 'touchenable',
    'textNot', 'typeNot',
)


def build_query(name, **attrs):
    for attr_name in attrs.keys():
        if attr_name not in QueryAttributeNames:
            raise Exception('Unsupported Attribute name for query  !!!')
    query = []
    if name is not None:
        attrs['name'] = name
    for attr_name, attr_val in attrs.items():
        if attr_name in ('textNot', 'typeNot'):
            attr_name = attr_name[:-3]
            op = 'attr!='
        else:
            op = 'attr='
        query.append((op, (attr_name, attr_val)))
    return 'and', tuple(query)


class UIObjectProxy(object):
    def __init__(self, poco, name=None, **attrs):
        self.query = build_query(name, **attrs)
        self.poco = poco
        self._negtive = False

    def child(self, name=None, **attrs):
        sub_query = build_query(name, **attrs)
        query = ('/', (self.query, sub_query))
        obj = UIObjectProxy(self.poco)
        obj.query = query
        return obj

    def offspring(self, name=None, **attrs):
        sub_query = build_query(name, **attrs)
        query = ('>', (self.query, sub_query))
        obj = UIObjectProxy(self.poco)
        obj.query = query
        return obj

    def sibling(self, name=None, **attrs):
        sub_query = build_query(name, **attrs)
        query = ('-', (self.query, sub_query))
        obj = UIObjectProxy(self.poco)
        obj.query = query
        return obj

    def __getitem__(self, item):
        obj = UIObjectProxy(self.poco)
        obj.query = ('index', (self.query, item))
        return obj

    def __len__(self):
        return self.attr('length')

    def __neg__(self):
        ret = UIObjectProxy(self.poco)
        ret.query = self.query
        ret._negtive = True
        return ret

    def __iter__(self):
        nodes = self.poco.selector.select(self.query)
        for n in nodes:
            yield n

    @retries_when(HunterRpcTimeoutException)
    def click(self, click_anchor=True, sleep_interval=None):
        pos = self.attr('anchorPosition') if click_anchor else self.attr('screenPosition')
        self.poco.touch(pos)
        if sleep_interval:
            time.sleep(sleep_interval)
        else:
            self.poco.wait_stable()

    def swipe(self, dir, distance_percent=0.1, duration=0.5):
        origin_pos = self.attr('anchorPosition')
        if dir == 'up':
            dir_vec = [0, -1 * distance_percent]
        elif dir == 'down':
            dir_vec = [0, distance_percent]
        elif dir == 'left':
            dir_vec = [-1 * distance_percent, 0]
        elif dir == 'right':
            dir_vec = [distance_percent, 0]
        elif type(dir) in (list, tuple):
            dir_vec = [dir[0] * distance_percent, dir[1] * distance_percent]
        else:
            raise TypeError('Unsupported direction type {}. '
                            'Only "up/down/left/right" or 2 elements list/tuple available.'.format(type(dir)))
        self.poco.swipe(origin_pos, direction=dir_vec, duration=duration)

    def wait_for_appearance(self, timeout=120):
        start = time.time()
        while not self.exists():
            self.poco.sleep_for_polling_interval()
            if time.time() - start > timeout:
                raise RuntimeError('Timeout at waiting for {} to appear'.format(repr(self.query)))

    def wait_for_disappearance(self, timeout=120):
        start = time.time()
        while self.exists():
            self.poco.sleep_for_polling_interval()
            if time.time() - start > timeout:
                raise RuntimeError('Timeout at waiting for {} to disappear'.format(repr(self.query)))

    @retries_when(HunterRpcTimeoutException)
    def attr(self, name):
        val = self.poco.selector.selectAndGetAttribute(self.query, name)
        if self._negtive:
            if type(val) is bool:
                return not val
            elif type(val) in (float, int, long):
                return -val
        return val

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
        text = self.attr('text')
        if type(text) is unicode:
            text = text.encode('utf-8')
        return text

    def get_name(self):
        return self.attr('name')

    def get_size(self):
        return self.attr('size')

    def __str__(self):
        return 'UIObjectProxy of "{}"'.format(self.query)
    __repr__ = __str__
