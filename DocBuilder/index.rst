
Welcome to Poco ポコ documentation!
================================

This document provides all the basic information that are needed to start using Poco ポコ cross-engine UI
automation framework. It covers the main framework ideas and concepts and shows examples for various use cases as well.


Getting Started
===============

.. toctree::
   :maxdepth: 2

   source/README

Install Poco and PocoSDK
------------------------

This section describes how to install `Poco` and `PocoSDK`.

**System Requirements**

* Operating System:
    * Windows
    * MacOS X
    * Linux

* Python2.7 & Python3.3+

**Installing the Python package**

In order to use Poco, you must install Poco python library on your host and also install the `poco-sdk`_ in
your game/app.

**Poco** can be installed straightforward with ``pip`` command

.. code-block:: bash

    # In the future
    pip install poco

Currently, the code is available only in `Git` repository and can be installed as follows

.. code-block:: bash

    git clone https://github.com/Meteorix/poco.git
    pip install -e poco

For NetEase internal use, clone the repository from following location

.. code-block:: bash

    git clone ssh://git@git-qa.gz.netease.com:32200/maki/poco.git
    pip install -e poco

For **poco-sdk** integration please refer to `Integration Guide`_


Using Poco as Python package
=============================

Simple demo
-----------

The following example shows a simple script on demo game using Unity3D. Check `More examples`_ section for more detailed
info.

.. code-block:: python

    from poco.drivers.unity3d import UnityPoco as Poco

    poco = Poco(('localhost', 5001))

    # tap start button
    poco('start_btn', type='Button').click()

    # collect all 'stars' to my 'bag' by dragging the star icon
    bag = poco('bag_area')
    for star in poco(type='MPanel').child('star'):
        star.drag_to(bag)

    # click Text starting with 'finish' to finish collecting
    poco(textMatches='finish.*').click()


Dump UI hierarchy example
--------------------------

Poco defines an uniform format to serialize UI hierarchy for different game engines. This section shows how to dump
UI hierarchy.

.. code-block:: python

    from poco.drivers.unity3d import UnityPoco as Poco
    from pprint import pprint

    poco = Poco()
    ui = poco.agent.hierarchy.dump()
    pprint(ui)



The following is the snippet of UI hierarchy. All UI elements are organized in `dict` representing the `tree` structure.
More detailed info about properties are described in
`README <source/poco.sdk.AbstractDumper.html#poco.sdk.AbstractDumper.IDumper.dumpHierarchy>`_.

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
    
    source/poco
    source/poco.proxy
    source/poco.exceptions
    source/poco.sdk


..
 下面的连接要替换成绝对路径

.. _poco-sdk: source/doc/integration.html
.. _Integration Guide: source/doc/integration.html
.. _More examples: source/doc/poco-example/index.html
.. _PocoUnit: http://git-qa.gz.netease.com/maki/PocoUnit

..
 下面是对应sdk的下载链接

.. _cocos2dx-js:
.. _android-native:
