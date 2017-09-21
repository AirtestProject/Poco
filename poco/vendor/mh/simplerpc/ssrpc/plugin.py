import inspect
from ..simplerpc import dispatcher, RpcAgent
from ..rpcclient import RpcClient
from ..rpcserver import RpcServer
from functools import partial


class PluginRepo(object):

    REPO = {}

    @classmethod
    def register(cls, plugin):
        cls.REPO[plugin.UUID] = plugin
        methods = inspect.getmembers(plugin, predicate=inspect.ismethod)
        for name, method in methods:
            if not name.startswith("_"):
                # add all plugin methods
                plugin_and_name = "_%s_%s" % (plugin.UUID, name)
                print("register rpc method", plugin_and_name, method)
                dispatcher.add_method(method, plugin_and_name)


class Plugin(object):

    UUID = None

    def _on_rpc_ready(self, agent):
        print("on_rpc_ready", self, agent)

    def _on_rpc_close(self, agent):
        print("on_rpc_close", self, agent)


class SSRpcClient(RpcClient):
    def on_connect(self):
        super(SSRpcClient, self).on_connect()
        agent = RemoteAgent(self, self.call)
        AgentManager.register(agent)
        for pid, plugin in PluginRepo.REPO.items():
            plugin._on_rpc_ready(agent)

    def on_close(self):
        super(SSRpcClient, self).on_close()
        agent = RemoteAgent(self, self.call)
        AgentManager.unregister(self)
        for pid, plugin in PluginRepo.REPO.items():
            plugin._on_rpc_close(agent)


class SSRpcServer(RpcServer):
    def on_client_connect(self, conn):
        super(SSRpcServer, self).on_client_connect(conn)
        agent = RemoteAgent(conn, partial(self.call, conn))

        print self.call(conn, "get_role").wait()  # 为什么这里会卡死！！！明天来看看

        def func(role):
            print(role)
            AgentManager.register(agent)

            for pid, plugin in PluginRepo.REPO.items():
                plugin._on_rpc_ready(agent)
        self.call(conn, "get_role").callback(func)

    def on_client_close(self, conn):
        super(SSRpcServer, self).on_client_close(conn)
        agent = AgentManager.find_agent(conn)
        AgentManager.unregister(agent)
        for pid, plugin in PluginRepo.REPO.items():
            plugin._on_rpc_close(agent)


class RemoteAgent(RpcAgent):
    def __init__(self, conn, rpccall):
        super(RemoteAgent, self).__init__()
        self.conn = conn
        self.rpccall = rpccall
        self.role = None

    def call(self, *args, **kwargs):
        return self.rpccall(*args, **kwargs)


class AgentManager(object):

    REPO = []
    ROLE = "CLIENT"

    @classmethod
    def register(cls, agent):
        cls.REPO.append(agent)
        print(cls.REPO)

    @classmethod
    def unregister(cls, agent):
        cls.REPO.remove(agent)

    @classmethod
    def find_agent(cls, conn):
        for i in cls.REPO:
            if i.conn == conn:
                return i
        return None


@dispatcher.add_method
def get_role():
    return AgentManager.ROLE
