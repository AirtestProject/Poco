
Welcome to Poco's documentation!
================================

**Poco is a cross-engine UI automation framework.**

Features
========

* Support mainstream game engines, like Unity3D, cocos2dx-js, cocos2dx-lua, Android native, etc.
* Super fast and impact-less to the game/app.
* Very easy to integrate sdk in the game/app.
* Simple powerful APIs across all engines.
* Support multi-touch (fling/pinch/etc.) (in development).
* Support gps, gyros, rotation (landscape/portrait) and other sensors as input (in development).
* Support retrieve UI properties and send text as input.
* Customizable by poco-sdk.
* Alternative rpc interface.
* No extra dependencies.
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



API reference
=============

Poco
----

.. toctree::
    :maxdepth: 1
    
    source/poco
    source/poco.proxy
    source/poco.exceptions


Poco SDK
--------

.. toctree::
    :maxdepth: 2
    :titlesonly:
    
    source/poco.sdk
    source/poco.sdk.interfaces
