# coding=utf-8
__author__ = 'lxn3032'


import time

from airtest.core.main import touch, swipe, snapshot
from airtest.cli.runner import device as current_device
from airtest_hunter import AirtestHunter, open_platform
from poco import Poco
from poco.exceptions import InvalidOperationException
from hunter_rpc import HunterRpc
from functools import wraps


class AirtestPoco(Poco):

    def __init__(self, process, hunter=None):
        apitoken = open_platform.get_api_token(process)
        self._hunter = hunter or AirtestHunter(apitoken, process)
        rpc_client = HunterRpc(self._hunter, self)
        super(AirtestPoco, self).__init__(rpc_client)

    def command(self, script, lang='text', sleep_interval=None):
        """
        通过hunter调用gm指令，可调用hunter指令库中定义的所有指令，也可以调用text类型的gm指令
        gm指令相关功能请参考safaia GM指令扩展模块

        :param script: 指令
        :param lang: 语言，默认text
        :param sleep_interval: 调用指令后的等待间隔时间
        :return: None
        """

        self._hunter.script(script, lang=lang)
        if sleep_interval:
            time.sleep(sleep_interval)
        else:
            self.wait_stable()
