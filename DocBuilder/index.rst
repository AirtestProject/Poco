
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
* Extensible to other private engines by implementing [poco-sdk]().
* Compatible with Python 2.7 and Python 3.3+.


Getting Started
===============

.. toctree::
   :maxdepth: 2

   source/README

Install Poco and PocoSDK
------------------------

To use poco, you should install poco in your host as a python library and install `poco-sdk <source/doc/integration.html>`_ in your game/app.

**poco** can be installed with pip::

    # In the future
    pip install poco

::

    # Currently, it is only available on git repo. So please clone the repo and install
    git clone xxx/poco.git
    pip install -e poco

**poco-sdk** integration please refer to `Integration Guide <source/doc/integration.html>`_


Example
=======

The following example shows a simple test script on demo game using Unity3D. `More examples are here <source/doc/poco-example/index.html>`_.
::

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
======================

Poco defines an uniform format to serialize ui heirarchy for different game engines. This section shows how to dump ui hierarchy.
::

    from poco.drivers.unity3d import UnityPoco as Poco
    from pprint import pprint

    poco = Poco()
    ui = poco.agent.hierarchy.dump()
    pprint(ui)



The following is part of ui heirarchy. All ui elements are organized in dict like tree structure. Properties are described in `README <source/README.html#basic-concepts>`_.
::

    ...
    {
        u'name': u'OctopusArea',
        u'payload': {u'anchorPoint': [0.5,
                                    0.5],
                   u'clickable': True,
                   u'name': u'OctopusArea',
                   u'pos': [0.130729169,
                            0.44907406],
                   u'scale': [1,
                              1],
                   u'size': [0.0859375,
                             0.125],
                   u'type': u'GameObject',
                   u'visible': True,
                   u'zOrders': {u'global': 0,
                                u'local': -10}}}],
        u'children': [{...}, {...}]
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
