
网易游戏项目测试脚本标准模板
==============

非网易游戏项目和unity3d项目请勿使用此工程模板。

游戏自动化测试是一项 **工程** ，不是离散的脚本，建议按照下面的方式组织脚本，有利于项目长久维护。

按照下面的指引组织好工程后，在testcase中使用 ``poco`` 对象可以简单地像下面这样获取

.. code-block:: python

    # 以runTest函数为例
    def runTest(self):
        self.poco('button').click()

安装网易专用依赖库
'''''''''

.. code-block:: bash

     pip install -i https://pypi.nie.netease.com/ airtest_hunter


目录结构
''''

.. code-block:: text

    ─ /
        ├─ lib/
        |   ├─ __init__.py
        |   ├─ case.py
        |   └─ player.py
        ├─ scripts/
        |   ├─ group/
        |   |   ├─ group_test1.air
        |   |   └─ group_test2.air
        |   ├─ test1.air
        |   |   └─ test1.py
        |   └─ test2.air
        |       └─ test2.py
        └─ launcher.py

``lib`` 目录用于存放公共代码模块和其他任何你需要的库。 ``scripts`` 目录用于存放一个个脚本文件，支持多级嵌套，用 ``.air`` 的文件夹后缀
组织每个脚本，这个目录里可以存放脚本引用到的所有资源文件，脚本运行结束后也会存储对应的运行结果文件。其余的目录没有规定，根据实际情况建立
自己需要的目录。

模板代码
''''

在自己本地新建文件并把下面代码copy到文件里。

``case.py``
-----------

case.py 里定义最基础的用例模板，全局初始化和清场行为。 **登录脚本除外** 。一般CommonCase里就是设置好player成员变量就行了，这样在每个
testcase里面可以方便地访问到player对象。

.. code-block:: python

    # coding=utf-8

    from pocounit.case import PocoTestCase
    from pocounit.addons.poco.action_tracking import ActionTracker
    from pocounit.addons.hunter.runtime_logging import AppRuntimeLogging

    from airtest.core.api import connect_device, device as current_device

    from player import Player


    class CommonCase(PocoTestCase):
        @classmethod
        def setUpClass(cls):
            super(CommonCase, cls).setUpClass()

            # 例如使用android手机进行测试
            if not current_device():
                connect_device('Android:///')

                # 如果连接windows的话，用下面这种写法
                # conncect_device('Windows:///?title_re=^.*标题栏正则.*$')

            cls.player = Player()

            action_tracker = ActionTracker(cls.player.poco)
            runtime_logger = AppRuntimeLogging(cls.player.hunter)
            cls.register_addin(action_tracker)
            cls.register_addin(runtime_logger)



``player.py``
-------------

player.py 里定义游戏测试中跟角色相关的行为和属性等，用于抽象隔离hunter、poco、airtest等库。测试脚本与测试框架细节隔离有利于兼容框架
后续的功能更新和升级，也能随时切换到别的框架上。

``class Player`` 中可以加入其余需要的自定义方法，例如常用的关闭所有窗口、打开背包等。

关于GM指令，默认通过hunter直接调用，可以改写成其他的方式。如果需要获取GM指令的返回值，请先了解GM指令的代码实现方式，再通过hunter-rpc
进行调用。

请将 ``PROCESS`` 变量改成对应的hunter项目代号。

.. code-block:: python

    # coding=utf-8

    import sys
    import re

    from airtest_hunter import AirtestHunter, open_platform, wait_for_hunter_connected
    from poco.drivers.netease.internal import NeteasePoco as Poco


    __all__ = ['Player']
    PROCESS = 'g62'  # hunter上的项目代号


    class Singleton(type):
        def __init__(cls, name, bases, dict):
            super(Singleton, cls).__init__(name, bases, dict)
            cls.instance = None

        def __call__(cls, *args, **kwargs):
            if cls.instance is None:
                cls.instance = super(Singleton, cls).__call__(*args, **kwargs)
            return cls.instance


    def get_hunter_instance():
        tokenid = open_platform.get_api_token(PROCESS)
        hunter = AirtestHunter(tokenid, PROCESS)
        return hunter


    class Player(object):
        __metaclass__ = Singleton

        def __init__(self, hunter=None):
            self._hunter = hunter or get_hunter_instance()
            self._poco_instance = None

        @property
        def poco(self):
            if not self._poco_instance:
                self._poco_instance = Poco(PROCESS, self._hunter)
            return self._poco_instance

        @property
        def hunter(self):
            return self._hunter

        def refresh(self):
            wait_for_hunter_connected(PROCESS, timeout=16)
            self._hunter = get_hunter_instance()
            self._poco_instance = Poco(PROCESS, self._hunter)

        def server_call(self, cmd):
            self.hunter.script(cmd, lang='text')


``test1.air/test1.py`` 模板
-------------------------

**请勿在测试脚本里使用任何全局变量来存储测试相关的对象！**

**请勿在测试脚本里使用任何全局变量来存储测试相关的对象！**

**请勿在测试脚本里使用任何全局变量来存储测试相关的对象！**


以下是例子， ``runTest`` 必须， ``setUp`` 和 ``tearDown`` 可选，根据实际需求选择。

.. code-block:: python

    from lib.case import CommonCase

    # 一个文件里建议就只有一个CommonCase
    # 一个Case做的事情尽量简单，不要把一大串操作都放到一起
    class MyTestCase(CommonCase):
        @property
        def poco(self):
            return self.player.poco

        @property
        def hunter(self):
            return self.player.hunter

        def setUp(self):
            # 调用hunter指令可以这样写
            self.hunter.script('print 23333', lang='python')

            # hunter rpc对象可以这样获取
            remote_obj = self.hunter.rpc.remote('uri-xxx')
            remote_obj.func1()

        def runTest(self):
            # 普通语句跟原来一样，但是必须都要用self开头，这是为了以后动态代理
            self.poco(text='角色').click()

            # 断言语句跟python unittest写法一模一样
            self.assertTrue(self.poco(text='最大生命').wait(3).exists(), "看到了最大生命")

            self.poco('btn_close').click()
            self.poco('movetouch_panel').offspring('point_img').swipe('up')

            self.assertTrue(False, '肯定错！')

        def tearDown(self):
            # 如果没有清场操作，这个函数就不用写出来
            a = 1 / 0


    # 固定格式
    if __name__ == '__main__':
        import pocounit
        pocounit.main()


如何运行脚本
''''''

就跟普通python脚本一样，直接运行即可

.. code-block:: bash

    python scripts/test1.air/test1.py

如果当前目录不在工程根目录，需要加上环境变量PROJECT_ROOT，假设工程根目录在 ``D:\project``

.. code-block:: bash

    set PROJECT_ROOT=D:\project & python test1.py

