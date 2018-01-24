# encoding=utf-8
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
                plugin_funcname = "_%s_%s" % (plugin.UUID, name)
                print("register rpc method", plugin_funcname, method)
                dispatcher.add_method(method, plugin_funcname)

    @classmethod
    def plugins_ready(cls, agent):
        def cb():
            AgentManager.register(agent)
            for pid, plugin in cls.REPO.items():
                plugin._on_rpc_ready(agent)
        agent.get_role_from_remote(cb)

    @classmethod
    def plugins_close(cls, agent):
        if not agent.registered:
            return
        AgentManager.unregister(agent)
        for pid, plugin in PluginRepo.REPO.items():
            plugin._on_rpc_close(agent)


class Plugin(object):

    UUID = None

    def _on_rpc_ready(self, agent):
        # print("on_rpc_ready", self, agent)
        pass

    def _on_rpc_close(self, agent):
        # print("on_rpc_close", self, agent)
        pass


class SSRpcClient(RpcClient):
    def on_connect(self):
        super(SSRpcClient, self).on_connect()
        agent = RemoteAgent(self, self.call)
        PluginRepo.plugins_ready(agent)

    def on_close(self):
        super(SSRpcClient, self).on_close()
        agent = AgentManager.get_agent_by_conn(self)
        if agent:
            PluginRepo.plugins_close(agent)


class SSRpcServer(RpcServer):
    def on_client_connect(self, conn):
        super(SSRpcServer, self).on_client_connect(conn)
        agent = RemoteAgent(conn, partial(self.call, conn))
        # 这里不要rpc.wait，会卡死，因为这个函数返回了连接才建立
        PluginRepo.plugins_ready(agent)

    def on_client_close(self, conn):
        super(SSRpcServer, self).on_client_close(conn)
        agent = AgentManager.get_agent_by_conn(conn)
        if agent:
            PluginRepo.plugins_close(agent)


class RemoteAgent(RpcAgent):
    def __init__(self, conn, rpccall):
        super(RemoteAgent, self).__init__()
        self.conn = conn
        self.rpccall = rpccall
        self.role = None
        self.registered = False

    def call(self, *args, **kwargs):
        return self.rpccall(*args, **kwargs)

    def get_role_from_remote(self, cb):
        def func(role):
            self.role = role
            cb()
        self.call("get_role").on_result(func)

    def get_plugin(self, uuid):
        return RemotePlugin(uuid, agent=self)


class AgentManager(object):

    REPO = []
    MAIN = None
    ROLE = None  # ["SERVER", "CLIENT", ...]

    @classmethod
    def register(cls, agent):
        cls.REPO.append(agent)
        if not cls.MAIN:
            cls.MAIN = agent
        agent.registered = True

    @classmethod
    def unregister(cls, agent):
        cls.REPO.remove(agent)
        if cls.MAIN == agent and cls.REPO:
            print("Main Agent Changed")
            cls.MAIN = cls.REPO[0]
        agent.registered = False

    @classmethod
    def get_agent_by_conn(cls, conn):
        for i in cls.REPO:
            if i.conn == conn:
                return i
        return None

    @classmethod
    def get_agents(cls, role=None):
        if role is None:
            return cls.REPO
        else:
            return [a for a in cls.REPO if a.role == role]

    @classmethod
    def set_main_agent(cls, agent):
        cls.MAIN = agent

    @classmethod
    def get_main_agent(cls):
        return cls.MAIN

    @staticmethod
    @dispatcher.add_method
    def get_role():
        """return role for remote"""
        return AgentManager.ROLE
    

class RemotePlugin(object):
    def __init__(self, uuid, agent=None, agent_filter=None):
        self._uuid = uuid
        self._agent = agent
        self._filter = agent_filter

    def _call_rpc(self, agent, funcname, *args, **kwargs):
        plugin_funcname = "_%s_%s" % (self._uuid, funcname)
        print(agent, plugin_funcname)
        return agent.call(plugin_funcname, *args, **kwargs)

    def _all(self, role=None):
        agent_filter = partial(AgentManager.get_agents, role)
        obj = RemotePlugin(self._uuid, agent_filter=agent_filter)
        return obj

    def _make_rpc_call(self, funcname, *args, **kwargs):
        if self._agent:
            return self._call_rpc(self._agent, funcname, *args, **kwargs)
        elif self._filter is None:
            return self._call_main_rpc(funcname, *args, **kwargs)
        else:
            agents = self._filter()
            cbs = []
            for agent in agents:
                cb = self._call_rpc(agent, funcname, *args, **kwargs)
                cbs.append(cb)
            # 返回cbs。。不太好，有更好的搞法吗？
            # cbs共用一个对象？各自callback？
            return cbs

    def _call_main_rpc(self, funcname, *args, **kwargs):
        agent = AgentManager.MAIN
        assert agent is not None, "Main Agent not set yet"
        return self._call_rpc(agent, funcname, *args, **kwargs)

    def __getattr__(self, funcname):
        def _call(*args, **kwargs):
            return self._make_rpc_call(funcname, *args, **kwargs)
        return _call
