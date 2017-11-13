
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

    # In the future
    pip install poco

Currently, the code is available only in `Git` repository and can be installed as follows. As airtest is a dependency
of poco, install airtest first.

.. code-block:: bash

    git clone https://github.com/Meteorix/airtest.git
    pip install -e airtest

    git clone https://github.com/Meteorix/poco.git
    pip install -e poco

For NetEase internal use, clone the repository from following location

.. code-block:: bash

    pip install --extra-index-url http://pypi.nie.netease.com/ --trusted-host pypi.nie.netease.com poco pocounit

For **poco-sdk** integration please refer to `Integration Guide`_


Using Poco as Python package
============================

Simple demo
-----------

The following example shows a simple script on demo game using Unity3D. Check `More examples`_ section for more detailed
info.

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

To retrieve the UI hierarchy of the game, please use our `AirtestIDE`_ (an IDE for writing test scripts) !

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
    
    source/poco.pocofw
    source/poco.proxy
    source/poco.exceptions
    source/poco.sdk


.. _poco-sdk: source/doc/integration.html
.. _Integration Guide: source/doc/integration.html
.. _More examples: source/doc/poco-example/index.html
.. _PocoUnit: http://git-qa.gz.netease.com/maki/PocoUnit
.. _AirtestIDE: 下载链接

..
 下面是对应sdk的下载链接

.. _cocos2dx-js:
.. _android-native:
