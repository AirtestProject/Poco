# encoding=utf-8
import sys
sys.path.append("../../..")
from simplerpc.ssrpc.plugin import PluginRepo, Plugin, SSRpcClient, AgentManager, RemotePlugin
from pprint import pprint


def test_client(c, c2):
    # simply call rpc
    print c.call("foobar", foo="aaa", bar="bbb").wait()


    RemoteAAA = RemotePlugin(AAAPlugin.UUID)
    print RemoteAAA.minus(555, 1).wait()
    print AgentManager.REPO

    print RemoteAAA._all().minus(555, 111)
    cbs = RemoteAAA._all("SERVER").minus(555, 222)
    for cb in cbs:
        print cb.wait(), cb.agent

    print RemoteAAA._all("SERVER2").minus(555, 333)

    AgentManager.set_main_agent(c2)
    cb = RemoteAAA.minus(555, 444)
    print cb.wait(), cb.agent

    AgentManager.set_main_agent(c)
    cb = RemoteAAA.minus(555, 444)
    print cb.wait(), cb.agent


class AAAPlugin(Plugin):

    UUID = "AAAAAAA"

    def _on_rpc_ready(self, agent):
        agent.get_plugin(self.UUID).minus(3, 5).on_result(pprint)
        agent.get_plugin(self.UUID).add(3, 5).on_error(pprint)
        agent.get_plugin("BBBBBBB").echo(3, 5).on_result(pprint)

    def add(self, a, b):
        return a + b


def test_ssrpc():
    from simplerpc.transport.tcp import TcpClient
    PluginRepo.register(AAAPlugin())
    AgentManager.ROLE = "CLIENT"

    client = TcpClient()
    c = SSRpcClient(client)
    # c.console_run({"c": c})
    c.run(backend=True)
    c.wait_connected()

    client2 = TcpClient()
    c2 = SSRpcClient(client2)
    c2.run(backend=True)
    c2.wait_connected()
    # #
    import time
    time.sleep(2)
    test_client(c, c2)
    time.sleep(200)


if __name__ == '__main__':
    test_ssrpc()
