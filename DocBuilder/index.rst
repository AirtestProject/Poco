
Welcome to Poco (ポコ) documentation!
===================================

This document provides all the basic information that are needed to start using Poco ポコ cross-engine UI
automation framework. It covers the main framework ideas and concepts and shows examples for various use cases as well.


Getting Started
===============

.. toctree::
   :maxdepth: 2

   source/README

Install Poco and PocoSDK
------------------------

In order to use Poco, you must install Poco python library on your host and also install the `poco-sdk`_ in
your game/app.

**Poco** can be installed straightforward with ``pip`` command

.. code-block:: bash

    pip install pocoui

For NetEase internal use, run the following command directly.

.. code-block:: bash

    pip install -i https://pypi.nie.netease.com/ airtest-hunter pocoui pocounit

For **poco-sdk** integration please refer to `Integration Guide`_


Using Poco as Python package
============================

Simple demo
-----------

The following example shows a simple script on demo game using Unity3D. Check `More examples`_ section for more detailed
info.

First you should connect your Android phone, for example, via usb cable and enable the **ADB DEBUG MODE**.

.. image:: ../doc/img/overview.gif

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

Tools for writing test scripts
------------------------------

To retrieve the UI hierarchy of the game, please use our `AirtestIDE`_ (an IDE for writing test scripts) or
standalone `PocoHierarchyViewer`_ (to viewer the hierarchy and attributes only but lightweight) !

Dump UI hierarchy example
-------------------------

Poco defines an uniform format to serialize UI hierarchy for different game engines. This section shows how to dump
UI hierarchy.

.. code-block:: python

    import json
    from poco.drivers.unity3d import UnityPoco as Poco

    poco = Poco()
    ui = poco.agent.hierarchy.dump()
    print(json.dumps(ui, indent=4))


The following is the snippet of UI hierarchy. All UI elements are organized in `dict` representing the `tree` structure.
More detailed info about properties are described in
`.dumpHierarchy() <source/poco.sdk.AbstractDumper.html#poco.sdk.AbstractDumper.IDumper.dumpHierarchy>`_.

.. code-block:: python

    ...
    {
        "name": "OctopusArea",
        "payload": {
            "name": "OctopusArea",
            "type": "GameObject",
            "visible": true,
            "clickable": true,
            "zOrders": {
                "global": 0,
                "local": -10
            },
            "scale": [
                1,
                1
            ],
            "anchorPoint": [
                0.5,
                0.5
            ],
            "pos": [
                0.130729169,
                0.44907406
            ],
            "size": [
                0.0859375,
                0.125
            ]
        }
        "children": [
            {...},
            ...
        ],
    }
    ...


API reference
=============

Poco
----

.. toctree::
    :maxdepth: 1

    source/poco.pocofw
    source/poco.proxy
    source/poco.exceptions
    source/poco.sdk

- `poco drivers <source/poco.drivers.html>`_

  - `Unity3D <source/poco.drivers.unity3d.unity3d_poco.html>`_
  - `cocos2dx-js <source/poco.drivers.cocosjs.html>`_
  - `android native <source/poco.drivers.android.uiautomation.html>`_
  - `Netease Games <source/poco.drivers.netease.internal.html>`_



.. _poco-sdk: source/doc/integration.html
.. _Integration Guide: source/doc/integration.html
.. _Integration Guide for NetEase: source/doc/integration.html#netease-internal-engines
.. _More examples: source/doc/poco-example/index.html
.. _Hunter内嵌inspector: source/doc/hunter-inspector-guide.html
.. _网易游戏项目测试脚本标准模板: source/doc/netease-internal-use-template.html
.. _PocoUnit: http://git-qa.gz.netease.com/maki/PocoUnit
.. _AirtestIDE: 下载链接
.. _PocoHierarchyViewer: http://init.nie.netease.com/downloads/poco/PocoHierarchyViewer-win32-x64.zip

..
 下面是对应sdk的下载链接

.. _cocos2dx-js:
.. _android-native:
