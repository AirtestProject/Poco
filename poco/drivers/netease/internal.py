# coding=utf-8

from airtest_hunter import open_platform, AirtestHunter
from hunter_cli.rpc.client import HunterRpcClient

from poco.pocofw import Poco
from poco.agent import PocoAgent
from poco.utils.airtest.input import AirtestInput
from poco.utils.airtest.screen import AirtestScreen
from poco.utils.hrpc.hierarchy import RemotePocoHierarchy
from poco.utils.hunter.command import HunterCommand
from poco.utils import six

__all__ = ['NeteasePoco']
__author__ = 'lxn3032'


class NeteasePocoAgent(PocoAgent):
    def __init__(self, hunter):
        client = hunter.rpc
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

        super(NeteasePocoAgent, self).__init__(hierarchy, input, screen, command)
        self._rpc_client = client


class NeteasePoco(Poco):
    def __init__(self, process, hunter=None, **options):
        if hunter:
            self._hunter = hunter
        else:
            apitoken = open_platform.get_api_token(process)
            self._hunter = AirtestHunter(apitoken, process)
        agent = NeteasePocoAgent(self._hunter)
        super(NeteasePoco, self).__init__(agent, **options)
        self._last_proxy = None
        self.screenshot_each_action = False
        if 'screenshot_each_action' in options:
            self.screenshot_each_action = options['screenshot_each_action']

    def on_pre_action(self, action, ui, args):
        if self.screenshot_each_action:
            # airteset log用
            from airtest.core.api import snapshot
            msg = repr(ui)
            if not isinstance(msg, six.text_type):
                msg = msg.decode('utf-8')
            snapshot(msg=msg)
