# coding=utf-8
__author__ = 'lxn3032'


import sys

from hunter_cli.device_output import trace


def default_formatter(data):
    return '[game-runtime] [{data[time]}] [{data[level]}] {data[data]}\n'.format(data=data)


def enable_tracing(tokenid, devid, file=None, formatter=default_formatter):
    if not file:
        file = sys.stdout
    elif not hasattr(file, 'write'):
        file = open(file)

    def _on_log(data):
        file.write(formatter(data))

    trace(tokenid, devid, _on_log)
