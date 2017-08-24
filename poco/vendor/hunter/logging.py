# coding=utf-8
__author__ = 'lxn3032'


import sys

from hunter_cli.device_output import trace


def default_formatter(data):
    return '[game-runtime] [{data[time]}] [{data[level]}] {data[data]}\n'.format(data=data)


def enable_tracing(tokenid, devid, central_server_url='http://hunter.nie.netease.com/webterm', file=None, formatter=default_formatter):
    if not file:
        file = sys.stdout
    elif not hasattr(file, 'write'):
        file = open(file)

    def _on_log(data):
        file.write(formatter(data))

    trace(tokenid, devid, central_server_url, _on_log)


class HunterLoggingMixin(object):
    """
    实时处理game-runtime log的mixin。需要self.hunter对象    
    """

    def __init__(self):
        super(HunterLoggingMixin, self).__init__()

    def start_log_tracing(self):
        # 通过device_info获取webterm的端点
        central_server_url = 'http://{}:{}/webterm'.format(*self.hunter.device_info.get('central_server_addr', ('192.168.40.111', 29003)))
        enable_tracing(self.hunter.tokenid, self.hunter.devid, central_server_url)
