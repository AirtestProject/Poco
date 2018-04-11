
网易游戏项目测试脚本标准模板
==============

内测功能，非网易游戏项目请勿使用此工程模板。

游戏自动化测试是一项 **工程** ，不是离散的脚本，建议按照下面的方式组织脚本，有利于项目长久维护。
而且还可以用pycharm直接打开工程，自动补全代码哦！

按照下面的指引组织好工程后，在testcase中使用 ``poco`` 对象可以简单地像下面这样获取

.. code-block:: python

    # 以runTest函数为例
    def runTest(self):
        self.poco('button').click()

安装网易专用依赖库
'''''''''

.. code-block:: bash

     pip install -i https://pypi.nie.netease.com/ airtest_hunter pocounit


目录结构
''''

.. code-block:: text

    ─ project_name/
        ├─ setup.py
        ├─ .gitignore
        ├─ res/
        |   └─ ..
        ├─ lib/
        |   ├─ __init__.py
        |   ├─ case.py
        |   └─ player.py
        └─ scripts/
            ├─ __init__.py
            ├─ test1.py
            └─ folder/
                ├─ __init__.py
                └─ test2.py

``lib`` 目录存放公共代码模块和其他任何你需要的库代码。 ``scripts`` 目录存放所有测试用例脚本文件， ``res`` 目录存放任意资源文件，没有
其他的规定了。

**如果你不想手动创建这些文件，请直接clone我们的** `工程模板repo`_ ， **然后给clone下来的文件夹改个名字（必须是标识符）并运行下面代码。**

.. code-block:: bash

    pip install -e <刚clone下来的文件夹名>

运行完之后看到一个叫 ``<刚clone下来的文件夹名>.egg-info`` 的文件夹就ok了。

模板代码
''''

在自己本地新建项目根文件夹， **记得给你的项目起一个好听的名字，例如g18_auto_project，命名必须是标识符** ，并把下面代码copy到文件夹
对应文件里。

``setup.py``
------------

setup.py 就是用来创建一个工程的，创建好这个文件后，可以直接在项目根文件夹下打开终端输入以下命令进行安装。如果你的项目依赖别的python包，
可以顺便新建个 ``requirements.txt`` 并在里面写上依赖其他第三方的模块。

.. code-block:: bash

    pip install -e .

setup.py 代码如下

.. code-block:: python

    # coding=utf-8

    import os
    import sys
    from setuptools import setup, find_packages
    from pip.req import parse_requirements

    current_frame = sys._getframe(0)
    caller = current_frame.f_back
    this_filename = caller.f_code.co_filename
    this_dir = os.path.abspath(os.path.join(this_filename, '..'))
    project_name = os.path.basename(this_dir)
    print('project name is {}'.format(project_name))


    if os.path.exists('requirements.txt'):
        # parse_requirements() returns generator of pip.req.InstallRequirement objects
        install_reqs = parse_requirements('requirements.txt', session=False)

        # reqs is a list of requirement
        reqs = [str(ir.req) for ir in install_reqs if ir.req]
    else:
        reqs = []

    setup(
        name=project_name,
        version='1.0.0',
        description='A test automation project using poco and pocounit.',
        packages=find_packages(),
        include_package_data=True,
        install_requires=reqs,
    )

``.gitignore``
--------------

这个大家都懂的

.. code-block:: text

    *.py[cod]

    # Packages
    *.egg
    *.egg-info
    dist
    build
    eggs
    parts
    bin
    var
    sdist
    develop-eggs
    .installed.cfg
    lib64
    __pycache__

    # Installer logs
    pip-log.txt

    # Unit test / coverage reports
    .coverage
    .tox
    nosetests.xml

    # Translations
    *.mo

    # Mr Developer
    .mr.developer.cfg
    .project
    .pydevproject
    .vs/
    tmp/
    *.log
    _site
    apps
    _build/
    *.spec
    htmlcov/
    cover/
    .idea/
    .DS_Store

    # test results
    log/
    pocounit-results/


``case.py``
-----------

case.py 里定义最基础的用例模板，全局初始化和清场行为。 **登录脚本除外** 。一般CommonCase里就是设置好player成员变量就行了，这样在每个
testcase里面可以方便地访问到player对象。

.. code-block:: python

    # coding=utf-8

    import os
    import sys

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
            cls.register_addon(action_tracker)
            cls.register_addon(runtime_logger)

        @property
        def poco(self):
            return self.player.poco

        @property
        def hunter(self):
            return self.player.hunter


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


``test1.py`` 举例
----------------

**请勿在测试用例的脚本里使用任何全局变量来存储测试相关的对象！**

**请勿在测试用例的脚本里使用任何全局变量来存储测试相关的对象！**

**请勿在测试用例的脚本里使用任何全局变量来存储测试相关的对象！**


以下是例子， ``runTest`` 必须， ``setUp`` 和 ``tearDown`` 可选，根据实际需求选择。

.. code-block:: python

    from lib.case import CommonCase

    # 一个文件里建议就只有一个CommonCase
    # 一个Case做的事情尽量简单，不要把一大串操作都放到一起
    class MyTestCase(CommonCase):
        def setUp(self):
            # 调用hunter指令可以这样写
            self.hunter.script('print 23333', lang='python')

            # hunter rpc对象可以这样获取
            remote_obj = self.hunter.rpc.remote('safaia-rpc-test')  # see http://hunter.nie.netease.com/mywork/instruction?insids=3086
            print(remote_obj.get_value())

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
            # 记得下面这句话是会报错的
            a = 1 / 0


    # 固定格式
    if __name__ == '__main__':
        import pocounit
        pocounit.main()


如何运行脚本
''''''

就跟普通python脚本一样，直接运行即可

.. code-block:: bash

    python scripts/test1.py


.. _工程模板repo: http://git-qa.gz.netease.com/maki/my_testwork
