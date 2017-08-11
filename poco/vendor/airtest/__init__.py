# coding=utf-8

from poco import Poco
from poco.agent import PocoAgent
from poco.vendor.airtest.hierarchy import RemotePocoHierarchy
from poco.vendor.airtest.input import AirtestInputer
from poco.vendor.airtest.screen import AirtestScreen
from poco.vendor.airtest.command import HunterCommand
from poco.vendor.airtest.logutil import airtestlog

from hunter_cli.rpc.client import HunterRpcClient
from airtest_hunter import AirtestHunter, open_platform


__author__ = 'lxn3032'


class AirtestPocoAgent(PocoAgent):
    def __init__(self, hunter):
        client = HunterRpcClient(hunter)
        client.set_timeout(25)
        remote_poco = client.remote('poco-uiautomation-framework-2')

        # hierarchy
        dumper = remote_poco.dumper
        selector = remote_poco.selector
        attributor = remote_poco.attributor
        hierarchy = RemotePocoHierarchy(dumper, selector, attributor)

        # input
        input = AirtestInputer()

        # screen
        screen = AirtestScreen(remote_poco.screen)

        # command
        command = HunterCommand(hunter)

        super(AirtestPocoAgent, self).__init__(hierarchy, input, screen, command)
        self._rpc_client = client

    def evaluate(self, obj_proxy):
        # TODO 临时方法，马上移除
        return self._rpc_client.evaluate(obj_proxy)


class AirtestPoco(Poco):

    def __init__(self, process, hunter=None):
        apitoken = open_platform.get_api_token(process)
        self._hunter = hunter or AirtestHunter(apitoken, process)
        agent = AirtestPocoAgent(self._hunter)
        super(AirtestPoco, self).__init__(agent)
        self._last_proxy = None

    def __call__(self, *args, **kwargs):
        ret = super(AirtestPoco, self).__call__(*args, **kwargs)

        # last proxy 暂时也只能记录到这一层的，proxy.child.child就不行了
        self._last_proxy = ret
        return ret

    @airtestlog
    def click(self, pos):
        super(AirtestPoco, self).click(pos)

    @airtestlog
    def swipe(self, p1, p2=None, direction=None, duration=2.0):
        super(AirtestPoco, self).swipe(p1, p2, direction, duration)

    @airtestlog
    def snapshot(self, width):
        return super(AirtestPoco, self).snapshot(width)
