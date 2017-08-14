# coding=utf-8
from poco import Poco
from poco.agent import PocoAgent
from poco.vendor.airtest.input import AirtestInput
from poco.vendor.airtest.screen import AirtestScreen
from poco.vendor.hrpc.hierarchy import RemotePocoHierarchy
from poco.vendor.hunter.command import HunterCommand

from airtest_hunter import AirtestHunter, open_platform
from hunter_cli.rpc.client import HunterRpcClient
from airtest.core.main import snapshot

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
        input = AirtestInput()

        # screen
        screen = AirtestScreen()

        # command
        command = HunterCommand(hunter)

        super(AirtestPocoAgent, self).__init__(hierarchy, input, screen, command)
        self._rpc_client = client


class AirtestPoco(Poco):
    def __init__(self, process, hunter=None):
        apitoken = open_platform.get_api_token(process)
        self._hunter = hunter or AirtestHunter(apitoken, process)
        agent = AirtestPocoAgent(self._hunter)
        super(AirtestPoco, self).__init__(agent)
        self._last_proxy = None

    def on_pre_action(self, action, proxy, args):
        # airteset log用
        snapshot(msg=unicode(proxy))
