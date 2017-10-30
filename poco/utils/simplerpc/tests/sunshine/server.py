# encoding=utf-8
import sys

sys.path.append("../../..")
from simplerpc.simplerpc import dispatcher, AsyncResponse
from simplerpc.ssrpc.plugin import PluginRepo, Plugin, SSRpcServer, AgentManager
from simplerpc.transport.tcp import TcpServer
from pprint import pprint


@dispatcher.add_method
def foobar(**kwargs):
    return kwargs["foo"] + kwargs["bar"]


class AAAPlugin(Plugin):
    UUID = "AAAAAAA"

    def _on_rpc_ready(self, agent):
        # print agent.get_plugin(self.UUID).add(3, 5).wait()
        agent.get_plugin(self.UUID).add(3, 5).on_result(pprint)

    def minus(self, a, b):
        return a - b


class BBBPlugin(Plugin):
    UUID = "BBBBBBB"

    def echo(self, *args):
        return args


def test_ssrpc():
    PluginRepo.register(AAAPlugin())
    PluginRepo.register(BBBPlugin())
    AgentManager.ROLE = "SERVER"
    s = SSRpcServer(TcpServer())
    s.run()
    # s.console_run({"s": s})

if __name__ == '__main__':
    test_ssrpc()
