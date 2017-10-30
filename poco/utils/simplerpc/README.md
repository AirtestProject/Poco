SimpleRPC
=====================
一种简单好用的RPC框架，扩展性强大，包含以下特性：

*   双向异步RPC调用
*   支持多条RPC连接
*   支持多种通信方式，内置提供python tcp/zmq/websocket
*   支持RPC ready/close事件
*   某一端可以既是server又是client，RPC api与通信方式无关
*   plugin系统支持定义不同的RPC服务，不同端的角色
*   封装成代理RemoteAgent，Api更清晰



## 基本使用方法
```Python
### client

from simplerpc.transport.tcp import TcpClient
from simplerpc.transport.sszmq import SSZmqClient
client = TcpClient()    # tcp连接
# client = SSZmqClient()    # sszmq连接
c = RpcClient(client)   # 构造rpc客户端
c.run(backend=True)    # 后台线程tick
c.wait_connected()  # 等待连接建立

# 最简单的调用
c.call("foobar", foo="aaa", bar="bbb")  

# 调用并等待返回值，wait返回(result,error)
cb = c.call("foo", foo=1, bar=2)   
r = cb.wait()   
print("wait and got:", r)
cb = c.call("make_error")   # 
r = cb.wait()
print("wait and got:", r)

# 调用并注册返回异步事件，on_result
c.call("foobar", foo="aaa", bar="bbb").on_result(pprint)
# 异步处理rpc错误，on_error
cb = c.call("foobar2", foo="aaa", bar="bbb")
cb.on_error(pprint)
cb.wait()


### server
from simplerpc.rpcserver import RpcServer
from simplerpc.transport.tcp import TcpServer
from simplerpc.transport.sszmq import SSZmqServer
s = RpcServer(TcpServer())
# s = RpcServer(SSZmqServer())
s.run()


### dispatcher
from simplerpc.simplerpc import dispatcher, AsyncResponse
import time

# 普通的rpc方法定义
@dispatcher.add_method
def foobar(**kwargs):
    return kwargs["foo"] + kwargs["bar"]

# 如果抛错，会返回在rpc的error中
@dispatcher.add_method
def make_error(*args):
    raise

# 异步返回rpc结果，也可以是异步抛出错误
@dispatcher.add_method
def delayecho(*args):
    r = AsyncResponse()
    from threading import Thread

    def func(r):
        time.sleep(5)
        r.result(args)
        # r.error(RuntimeError("something wrong here"))

    Thread(target=func, args=(r,)).start()
    return r
```

## Sunshine插件系统

```Python
### 定义插件
from simplerpc.ssrpc.plugin import PluginRepo, Plugin, SSRpcServer, AgentManager

class AAAPlugin(Plugin):
    UUID = "AAAAAAA"  # UUID用于找到远端对应的插件

    def _on_rpc_ready(self, agent):
        # print agent.get_plugin(self.UUID).add(3, 5).wait()
        agent.get_plugin(self.UUID).add(3, 5).on_result(pprint)

    def minus(self, a, b):
        return a - b

class BBBPlugin(Plugin):
    UUID = "BBBBBBB"

    def echo(self, *args):
        return args


PluginRepo.register(AAAPlugin())
PluginRepo.register(BBBPlugin())
AgentManager.ROLE = "SERVER"
s = SSRpcServer(TcpServer())
s.run()

### 远端调用插件
client = TcpClient()
c.run(backend=True)
c.wait_connected()

# 取远端默认远端对象的插件
RemoteAAA = RemotePlugin(AAAPlugin.UUID)
# 调用插件方法
print RemoteAAA.minus(555, 1).wait()

# 取所有远端对象
print AgentManager.REPO
# 调用所有远端对象方法
print RemoteAAA._all().minus(555, 111)
cbs = RemoteAAA._all("SERVER").minus(555, 222)
# 分别指定callback
for cb in cbs:
    print cb.wait(), cb.agent

# 切换默认远端对象
AgentManager.set_main_agent(c)
cb = RemoteAAA.minus(555, 444)
print cb.wait(), cb.agent

```

