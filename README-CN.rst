
Poco ポコ
=======

**A cross-engine UI automation framework**

Example
-------

.. image:: doc/img/overview.gif

.. code-block:: python

    # coding=utf-8

    import time
    from poco.drivers.unity3d import UnityPoco
    from airtest.core.api import connect_device

    # you should connect an Android device to your PC/mac
    # and set the ip address of your Android device
    connect_device('Android:///')
    poco = UnityPoco(('10.254.44.76', 5001))

    poco('btn_start').click()
    time.sleep(1.5)

    shell = poco('shell').focus('center')
    for star in poco('star'):
        star.drag_to(shell)
    time.sleep(1)

    assert poco('scoreVal').get_text() == "100", "score correct."
    poco('btn_back', type='Button').click()

`More examples`_ here.

Android原生应用或Unity3D游戏请使用 `HierarchyViewer`_ 查看UI层次结构，编写脚本请使用我们专门为您打造的 `AirtestIDE`_ 。

文档(Documentation)
-----------------

`在线文档`_ 。

安装(Installation)
----------------

直接运行下面的指令即可

::

    pip install -i https://pypi.nie.netease.com/ airtest-hunter poco pocounit

SDK接入(Integration)
------------------

网易内部项目无需嵌入sdk，请见 `接入指引 <#netease-integration-guide>`_

如何使用poco
--------

根据你所使用的引擎，按对应的方式初始化Poco实例。

* Unity3D

.. code-block:: python

    from poco.drivers.unity3d import UnityPoco
    from airtest.core.api import connect_device

    # you should connect an Android device to your PC/mac
    # and set the ip address of your Android device
    connect_device('Android:///')
    poco = UnityPoco(('10.254.44.76', 5001))

    # for windows
    # poco = UnityPoco(('localhost', 5001), editor_mode=True)

    ui = poco('...')
    ui.click()

* `NetEase Internal Engines <poco.drivers.netease.internal.html>`_ 公司内非Unity3D项目

.. code-block:: python

    from poco.drivers.netease.internal import NeteasePoco
    from airtest.core.api import connect_device

    # 先连上android设备
    connect_device('Android:///')

    # windows的话这样
    # connect_device('Windows:///?title_re=^.*errors and.*$')  # 无需urlencode

    poco = NeteasePoco('g37')  # hunter上的项目代号
    ui = poco('...')
    ui.click()

* `cocos2dx-js`_
* `android-native`_
* unreal (开发中)
* (others see `Integration guide`_ for more details)


对象选择与操作
-------

基本选择器
"""""

``poco`` 对象的 ``__call__`` 方法就是进行选择，遍历整个渲染树形结构，选出所有满足给定的属性的对象代理。第一个参数为节点名，其余的属性键值对通过命名参数传入。具体可参考 `API Reference`_ 。

.. code-block:: python

    # 根据节点名选择
    poco('bg_mission')

    # 节点名和属性选择
    poco('bg_mission', type='Button')
    poco(textMatches='^据点.*$', type='Button', enable=True)


.. image:: doc/img/hunter-poco-select-simple.png


相对选择器
""""""""

直接通过节点名或节点类型选择的对象容易产生歧义或无法选择时，可通过相对的方式按层级进行选择

.. code-block:: python

    # 直系孩子/后代选择
    poco('main_node').child('list_item').offspring('item')


.. image:: doc/img/hunter-poco-select-relative.png

顺序选择器（索引选择器，更推荐迭代遍历）
""""""""""""""""""""""""""""""""""

索引和遍历会默认按照从左到右从上到下的空间顺序按顺序遍历。遍历过程中，还未遍历到的节点如果从画面中移除了则会抛出异常，
已遍历的节点即使移除也不受影响。遍历顺序在遍历开始前已经确定，遍历过程中界面上的节点进行了重排则仍然按照之前的顺序进行遍历。

.. code-block:: python

    items = poco('main_node').child('list_item').offspring('item')
    print(items[0].child('material_name').get_text())
    print(items[1].child('material_name').get_text())


.. image:: doc/img/hunter-poco-select-sequence.png

遍历对象集合
""""""""""

.. code-block:: python

    # 遍历每一个商品
    items = poco('main_node').child('list_item').offspring('item')
    for item in items:
        item.child('icn_item')


.. image:: doc/img/hunter-poco-iteration.png

获取对象属性
""""""""""

.. code-block:: python

    mission_btn = poco('bg_mission')
    print(mission_btn.attr('type'))  # 'Button'
    print(mission_btn.get_text())  # '据点支援'
    print(mission_btn.attr('text'))  # '据点支援'，与get_text方法等价
    print(mission_btn.exists())  # True，表示是否存在界面中


对象代理操作
""""""

click
'''''

点击对象，默认以锚点(挂接点)(anchorPoint)对象为点击点。第一个参数传入点击相对位置，对象包围盒左上角为 ``[0, 0]`` ，右下角为 ``[1, 1]`` 。偏移范围可以比0小也可以比1大，超过0~1的范围表示超出包围盒范围。

.. code-block:: python

    poco('bg_mission').click()
    poco('bg_mission').click('center')
    poco('bg_mission').click([0.5, 0.5])    # 等价于center
    poco('bg_mission').focus([0.5, 0.5]).click()  # 等价于上面的表达式


.. image:: doc/img/hunter-poco-click.png

swipe
'''''

以对象anchor为起点，朝某个方向滑动一段距离

.. code-block:: python

    joystick = poco('movetouch_panel').child('point_img')
    joystick.swipe('up')
    joystick.swipe([0.2, -0.2])  # 向右上方45度滑动sqrt(0.08)单位距离
    joystick.swipe([0.2, -0.2], duration=0.5)


.. image:: doc/img/hunter-poco-swipe.png

drag
''''

从当前对象拖拽到目标对象

.. code-block:: python

    poco(text='突破芯片').drag_to(poco(text='岩石司康饼'))


.. image:: doc/img/hunter-poco-drag.png

focus (局部定位)
''''''''''''''

与节点坐标相关的操作默认以anchor为起始点，click的话就直接click在anchor上。如果要进行局部的点击偏移，可以使用focus操作。
focus同屏幕坐标系类似，以节点包围盒左上角为原点，长宽均为1，中心点即为 ``[0.5, 0.5]`` ，右下角为 ``[1, 1]`` ，以此类推。

.. code-block:: python

    poco('bg_mission').focus('center').click()  # 点击中心点



focus也可以用于一个对象的内部定位，例如实现一个ScrollView的卷动操作

.. code-block:: python

    scrollView = poco(type='ScollView')
    scrollView.focus([0.5, 0.8]).drag_to(scrollView.focus([0.5, 0.2]))


wait
''''

等待目标对象出现，总是返回对象自身，如果出现立即返回，否则timeout后返回

.. code-block:: python

    poco('bg_mission').wait(5).click()  # 最多等待5秒，出现即点击
    poco('bg_mission').wait(5).exists()  # 最多等待5秒，返回是否exists


捕获异常
----

.. code-block:: python

    from poco.exceptions import PocoTargetTimeout

    try:
        poco('guide_panel', type='ImageView').wait_for_appearance()
    except PocoTargetTimeout:
        # 面板没有弹出来，有bug
        raise


.. code-block:: python

    from poco.exceptions import PocoNoSuchNodeException

    img = poco('guide_panel', type='ImageView')
    try:
        if not img.exists():
            img.click()
    except PocoNoSuchNodeException:
        # 尝试对不存在的节点进行操作，会抛出此异常
        pass


单元测试
----

poco是自动化框架，关于单元测试请见 `PocoUnit`_ 。PocoUnit提供了一整套完整的断言方法，并且和python标准库unittest是兼容的。


Netease Integration Guide 接入参考
------------------------------

1. safaia版本需要高于1.2.0，如果不高于的话项目组master可在 `项目 <http://hunter.nie.netease.com/mywork/project#/>`_ 页直接下载
   最新版的接入模块。最近新注册的hunter项目一般不需要重新下载。
2. 在项目的 ``Hunter __init__指令`` 后面根据引擎插入以下代码片段，然后重启游戏即可，lua脚本的游戏请联系 ``lxn3032@corp.netease.com`` 。

**NeoX:**

.. code-block:: python

    # poco uiautomation
    PocoUiautomation = require('support.poco.neox.uiautomation')
    Safaia().install(PocoUiautomation)

    # inspector extension
    InspectorExt = require('support.poco.safaia.inspector')
    InspectorExt.screen = require('support.poco.neox.screen')()
    InspectorExt.dumper = require('support.poco.neox.Dumper')()
    Safaia().install(InspectorExt)

**Messiah:**

.. code-block:: python

    # poco uiautomation
    PocoUiautomation = require('support.poco.messiah.uiautomation')
    Safaia().install(PocoUiautomation)

    # inspector extension
    InspectorExt = require('support.poco.safaia.inspector')
    InspectorExt.screen = require('support.poco.messiah.screen')()   # 引擎自身原因，可能截图速度较慢
    InspectorExt.dumper = require('support.poco.cocos2dx.Dumper')()  # 3D 场景模型需另外适配
    Safaia().install(InspectorExt)

`Unity3D <doc/integration.html#unity3d>`_


**其他引擎:** 请联系 ``lxn3032@corp.netease.com``


3. `hunter终端`_ 右上角点击 **Inspector** 按钮打开检视器面板。



基本概念(concepts)
--------------


测试Test
""""""

* **TestCase**: 无论以何种形式表示的测试内容的一个单元，以下均指使用Poco编写的测试脚本
* **TestSuite**: 多个TestCase或TestSuite构成的一系列脚本文件
* **TestRunner**: 用于启动测试的一个东西，可能是一个可执行文件也可以是一个class。Poco默认使用Airtest作为TestRunner，使用Airtest启动的测试需要安装Airtest环境
* **TestTarget/TargetDevice**: 运行待测应用程序的设备，以下均指运行在手机上的待测游戏或PC版待测游戏

* **TestFramework**:  测试框架，Poco就是一个测试框架
* **TestFrameworkSDK**:  测试框架与待测应用集成的模块，一般来说不是必须的，Poco里带有一个SDK


Poco测试框架相关
""""""""""

* **目标设备**: 待测应用或游戏运行的机器，一般指手机
* **UI代理(UI proxy)**: poco框架内代表游戏内0个1个或多个UI元素的代理对象
* **节点/UI元素(Node/UI element)**: 应用/游戏内UI元素的实例，就是平时所说的UI
* **选择器(选择表达式)(query condition/expression)**: 一个可序列化的数据结构，poco通过该表达式与**目标设备**交互并选出其代表的对应的UI元素。Tester一般不用关心这个表达式的内部结构，除非要自定义`Selector`类。

.. image:: doc/img/hunter-inspector.png
.. image:: doc/img/hunter-inspector-text-attribute.png
.. image:: doc/img/hunter-inspector-hierarchy-relations.png

坐标系与度量空间定义
"""""""""""""""""

.. image:: doc/img/hunter-poco-coordinate-system.png

归一化坐标系
''''''''''

归一化坐标系就是将屏幕宽和高按照单位一来算，这样UI在poco中的宽和高其实就是相对于屏幕的百分比大小了，好处就是不同分辨率设备之间，同一个UI的归一化坐标系下的位置和尺寸是一样的，有助于编写跨设备测试用例。

归一化坐标系的空间是均匀的，屏幕正中央一定是(0.5, 0.5)，其他标量和向量的计算方法同欧式空间。

局部坐标系（局部定位）
'''''''''''

引入局部坐标系是为了表示相对于某UI的坐标。局部坐标系以UI包围盒左上角为原点，向右为x轴，向下为y轴，包围盒宽和高均为单位一。其余的定义和归一化坐标系类似。

局部坐标系可以更灵活地定位UI内或外的位置，例如(0.5, 0.5)就代表UI的正中央，超过1或小于0的坐标值则表示UI的外面。



.. _English README: README.rst
.. _hunter: http://hunter.nie.netease.com
.. _deploy-key: http://init.nie.netease.com/downloads/deploy/deploy-key
.. _hunter终端: http://hunter.nie.netease.com

..
 下面的连接要替换成绝对路径

.. _poco-sdk: doc/integration.html
.. _Integration Guide: doc/integration.html
.. _More examples: doc/poco-example/index.html
.. _PocoUnit: http://git-qa.gz.netease.com/maki/PocoUnit
.. _API Reference: http://init.nie.netease.com/autodoc/poco/doc-auto/index.html#api-reference
.. _在线文档: http://init.nie.netease.com/autodoc/poco/doc-auto/index.html
.. _HierarchyViewer: http://init.nie.netease.com/downloads/poco/PocoHierarchyViewer-win32-x64.zip
.. _AirtestIDE:

..
 下面是对应sdk的下载链接

.. _cocos2dx-js:
.. _android-native:
