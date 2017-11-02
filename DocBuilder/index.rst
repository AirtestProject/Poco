
Welcome to Poco's documentation!
================================

**Poco is a cross-engine UI automation framework.**

Features
========

* Support mainstream game engines, including: Unity3D, cocos2dx-js, cocos2dx-lua and Android native apps.
* Retrieve UI Elements Hierarchy in game's runtime.
* Super fast and impact-free to the game.
* Super easy sdk integration to the game in 5 minutes.
* Powerful APIs which are engine independent.
* Support multi-touch e.g. fling/pinch/etc. (in development)
* Support gps, gyros, rotation (landscape/portrait) and other sensors as input.  (in development)
* Extensible to other private engines by implementing `poco-sdk`_.
* Compatible with Python 2.7 and Python 3.3+.


Getting Started
===============

.. toctree::
   :maxdepth: 2

   source/README

Install Poco and PocoSDK
------------------------

To use poco, you should install poco in your host as a python library and install `poco-sdk`_ in your game/app.

**poco** can be installed with pip

.. code-block:: bash

    # In the future
    pip install poco

Currently, it is only available in git repo. So please clone the repo and install

.. code-block:: bash

    git clone https://github.com/Meteorix/poco.git
    pip install -e poco

For NetEase internally use, please execute the following command.

.. code-block:: bash

    git clone ssh://git@git-qa.gz.netease.com:32200/maki/poco.git
    pip install -e poco

**poco-sdk** integration please refer to `Integration Guide`_


Example
=======

The following example shows a simple test script on demo game using Unity3D. `More examples`_ are here.

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


Dump UI Hierarchy
=================

Poco defines an uniform format to serialize ui heirarchy for different game engines. This section shows how to dump ui hierarchy.

.. code-block:: python

    from poco.drivers.unity3d import UnityPoco as Poco
    from pprint import pprint

    poco = Poco()
    ui = poco.agent.hierarchy.dump()
    pprint(ui)



The following is part of ui heirarchy. All ui elements are organized in dict like tree structure. Properties are described in `README <source/poco.sdk.AbstractDumper.html#poco.sdk.AbstractDumper.IDumper.dumpHierarchy>`_.

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
