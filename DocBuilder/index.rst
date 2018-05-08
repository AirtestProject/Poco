
Welcome to Poco (ポコ) documentation!
===================================

**A cross-engine UI automation framework**. ``Unity3D``/``cocos2dx-*``/``Android native APP``/(Other engines SDK)/...

.. raw:: html

    <a href="https://github.com/AirtestProject/Poco" class="github-corner" aria-label="View source on Github">
        <svg width="120" height="120" viewBox="0 0 250 250" style="fill:#151513; color:#fff; position: fixed; top: 0; border: 0; right: 0;" aria-hidden="true">
            <path d="M0,0 L115,115 L130,115 L142,142 L250,250 L250,0 Z"></path>
            <path d="M128.3,109.0 C113.8,99.7 119.0,89.6 119.0,89.6 C122.0,82.7 120.5,78.6 120.5,78.6 C119.2,72.0 123.4,76.3 123.4,76.3 C127.3,80.9 125.5,87.3 125.5,87.3 C122.9,97.6 130.6,101.9 134.4,103.2" fill="currentColor" style="transform-origin: 130px 106px;" class="octo-arm"></path>
            <path d="M115.0,115.0 C114.9,115.1 118.7,116.5 119.8,115.4 L133.7,101.6 C136.9,99.2 139.9,98.4 142.2,98.6 C133.8,88.0 127.5,74.4 143.8,58.0 C148.5,53.4 154.0,51.2 159.7,51.0 C160.3,49.4 163.2,43.6 171.4,40.1 C171.4,40.1 176.1,42.5 178.8,56.2 C183.1,58.6 187.2,61.8 190.9,65.4 C194.5,69.0 197.7,73.2 200.1,77.6 C213.8,80.2 216.3,84.9 216.3,84.9 C212.7,93.1 206.9,96.0 205.4,96.6 C205.1,102.4 203.0,107.8 198.3,112.5 C181.9,128.9 168.3,122.5 157.7,114.1 C157.9,116.9 156.7,120.9 152.7,124.9 L141.0,136.5 C139.8,137.7 141.6,141.9 141.8,141.8 Z" fill="currentColor" class="octo-body"></path>
        </svg>
    </a>
    <style>
        .github-corner:hover .octo-arm {
            animation:octocat-wave 560ms ease-in-out
        }

        @keyframes octocat-wave {
            0%,100% {
                transform:rotate(0)
            }
            20%,60% {
                transform:rotate(-25deg)
            }
            40%,80% {
                transform:rotate(10deg)
            }
        }

        @media (max-width:500px) {
            .github-corner:hover .octo-arm {
                animation:none
            }
            .github-corner .octo-arm {
                animation:octocat-wave 560ms ease-in-out
            }
        }
    </style>

.. raw:: html

    <div style="height:40px;">
        <style>.github-btn{height:20px;overflow:hidden}.gh-btn,.gh-count,.gh-ico{float:left}.gh-btn,.gh-count{padding:2px 5px 2px 4px;color:#333;text-decoration:none;text-shadow:0 1px 0 #fff;white-space:nowrap;cursor:pointer;border-radius:3px}.gh-btn{background-color:#eee;background-image:-webkit-gradient(linear,left top,left bottom,color-stop(0,#fcfcfc),color-stop(100%,#eee));background-image:-webkit-linear-gradient(top,#fcfcfc 0,#eee 100%);background-image:-moz-linear-gradient(top,#fcfcfc 0,#eee 100%);background-image:-ms-linear-gradient(top,#fcfcfc 0,#eee 100%);background-image:-o-linear-gradient(top,#fcfcfc 0,#eee 100%);background-image:linear-gradient(to bottom,#fcfcfc 0,#eee 100%);filter:progid:DXImageTransform.Microsoft.gradient(startColorstr='#fcfcfc', endColorstr='#eeeeee', GradientType=0);background-repeat:no-repeat;border:1px solid #d5d5d5}.gh-btn:focus,.gh-btn:hover{text-decoration:none;background-color:#ddd;background-image:-webkit-gradient(linear,left top,left bottom,color-stop(0,#eee),color-stop(100%,#ddd));background-image:-webkit-linear-gradient(top,#eee 0,#ddd 100%);background-image:-moz-linear-gradient(top,#eee 0,#ddd 100%);background-image:-ms-linear-gradient(top,#eee 0,#ddd 100%);background-image:-o-linear-gradient(top,#eee 0,#ddd 100%);background-image:linear-gradient(to bottom,#eee 0,#ddd 100%);filter:progid:DXImageTransform.Microsoft.gradient(startColorstr='#eeeeee', endColorstr='#dddddd', GradientType=0);border-color:#ccc}.gh-btn:active{background-image:none;background-color:#dcdcdc;border-color:#b5b5b5;box-shadow:inset 0 2px 4px rgba(0,0,0,.15)}.gh-ico{width:14px;height:14px;margin-right:4px;background-image:url(data:image/svg+xml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHhtbG5zOnhsaW5rPSJodHRwOi8vd3d3LnczLm9yZy8xOTk5L3hsaW5rIiB2ZXJzaW9uPSIxLjEiIGlkPSJMYXllcl8xIiB4PSIwcHgiIHk9IjBweCIgd2lkdGg9IjQwcHgiIGhlaWdodD0iNDBweCIgdmlld0JveD0iMTIgMTIgNDAgNDAiIGVuYWJsZS1iYWNrZ3JvdW5kPSJuZXcgMTIgMTIgNDAgNDAiIHhtbDpzcGFjZT0icHJlc2VydmUiPjxwYXRoIGZpbGw9IiMzMzMzMzMiIGQ9Ik0zMiAxMy40Yy0xMC41IDAtMTkgOC41LTE5IDE5YzAgOC40IDUuNSAxNS41IDEzIDE4YzEgMC4yIDEuMy0wLjQgMS4zLTAuOWMwLTAuNSAwLTEuNyAwLTMuMiBjLTUuMyAxLjEtNi40LTIuNi02LjQtMi42QzIwIDQxLjYgMTguOCA0MSAxOC44IDQxYy0xLjctMS4yIDAuMS0xLjEgMC4xLTEuMWMxLjkgMC4xIDIuOSAyIDIuOSAyYzEuNyAyLjkgNC41IDIuMSA1LjUgMS42IGMwLjItMS4yIDAuNy0yLjEgMS4yLTIuNmMtNC4yLTAuNS04LjctMi4xLTguNy05LjRjMC0yLjEgMC43LTMuNyAyLTUuMWMtMC4yLTAuNS0wLjgtMi40IDAuMi01YzAgMCAxLjYtMC41IDUuMiAyIGMxLjUtMC40IDMuMS0wLjcgNC44LTAuN2MxLjYgMCAzLjMgMC4yIDQuNyAwLjdjMy42LTIuNCA1LjItMiA1LjItMmMxIDIuNiAwLjQgNC42IDAuMiA1YzEuMiAxLjMgMiAzIDIgNS4xYzAgNy4zLTQuNSA4LjktOC43IDkuNCBjMC43IDAuNiAxLjMgMS43IDEuMyAzLjVjMCAyLjYgMCA0LjYgMCA1LjJjMCAwLjUgMC40IDEuMSAxLjMgMC45YzcuNS0yLjYgMTMtOS43IDEzLTE4LjFDNTEgMjEuOSA0Mi41IDEzLjQgMzIgMTMuNHoiLz48L3N2Zz4=);background-size:100% 100%;background-repeat:no-repeat}.gh-count{position:relative;display:none;margin-left:4px;background-color:#fafafa;border:1px solid #d4d4d4}.gh-count:focus,.gh-count:hover{color:#4183C4}.gh-count:after,.gh-count:before{content:'';position:absolute;display:inline-block;width:0;height:0;border-color:transparent;border-style:solid}.gh-count:before{top:50%;left:-3px;margin-top:-4px;border-width:4px 4px 4px 0;border-right-color:#fafafa}.gh-count:after{top:50%;left:-4px;z-index:-1;margin-top:-5px;border-width:5px 5px 5px 0;border-right-color:#d4d4d4}.github-btn-large{height:30px}.github-btn-large .gh-btn,.github-btn-large .gh-count{padding:3px 10px 3px 8px;font-size:16px;line-height:22px;border-radius:4px}.github-btn-large .gh-ico{width:20px;height:20px}.github-btn-large .gh-count{margin-left:6px}.github-btn-large .gh-count:before{left:-5px;margin-top:-6px;border-width:6px 6px 6px 0}.github-btn-large .gh-count:after{left:-6px;margin-top:-7px;border-width:7px 7px 7px 0}</style>
        <span class="github-btn github-forks" id="github-btn" style="font:700 11px/14px 'Helvetica Neue',Helvetica,Arial,sans-serif">
            <a class="gh-btn" id="gh-btn" href="https://github.com/AirtestProject/Poco/fork" target="_blank" aria-label="Fork on GitHub">
                <span class="gh-ico" aria-hidden="true"></span> <span class="gh-text" id="gh-text">Fork</span>
            </a>
        </span>
        <span class="github-btn github-stargazers" id="github-btn" style="font:700 11px/14px 'Helvetica Neue',Helvetica,Arial,sans-serif">
            <a class="gh-btn" id="gh-btn" href="https://github.com/AirtestProject/Poco" target="_blank" aria-label="Star on GitHub" style="margin-left:4px;">
                <span class="gh-ico" aria-hidden="true"></span>
                <span class="gh-text" id="gh-text">Star</span>
            </a>
            <a class="gh-count" id="gh-count" href="https://github.com/AirtestProject/Poco/stargazers" target="_blank" aria-label="99+ stargazers on GitHub" style="display: block;">99+</a>
        </span>
    </div>

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

    poco = UnityPoco()

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

.. image:: source/doc/img/hunter-inspector.png

Tutorials and examples
----------------------

* `basic usage`_
* `interact with Buttons and Labels`_
* `drag and swipe operations`_
* `advanced selections`_
* `play with coordinate system and local positioning`_
* `iteration over elements`_
* `handling exceptions`_
* `waiting for events`_
* `play with unittest framework`_
* `optimize speed by freezing UI`_

.. _basic usage: source/doc/poco-example/basic.html
.. _interact with Buttons and Labels: source/doc/poco-example/interact_with_buttons_and_labels.html
.. _drag and swipe operations: source/doc/poco-example/drag_and_swipe_operations.html
.. _advanced selections: source/doc/poco-example/advanced_selections.html
.. _play with coordinate system and local positioning: source/doc/poco-example/play_with_coordinate_system_and_local_positioning.html
.. _iteration over elements: source/doc/poco-example/iteration_over_elements.html
.. _handling exceptions: source/doc/poco-example/handling_exceptions.html
.. _waiting for events: source/doc/poco-example/waiting_events.html
.. _play with unittest framework: source/doc/poco-example/play_with_unittest_framework.html
.. _optimize speed by freezing UI: source/doc/poco-example/optimize_speed_by_freezing_UI.html

API reference
=============

Poco API
--------

You can find all functions/methods for writing test scripts under the following links.

.. toctree::
    :maxdepth: 2

    Poco instance API <source/poco.pocofw>
    UI proxy object API <source/poco.proxy>
    Exceptions <source/poco.exceptions>

Engine specific API
'''''''''''''''''''

.. toctree::
    :hidden:

    Poco drivers (engine specific poco implementation) <source/doc/poco_drivers>

- `poco drivers (engine specific poco implementation) <source/doc/poco_drivers.html>`_

  - `Unity3D <source/poco.drivers.unity3d.unity3d_poco.html>`_
  - `Android native app <source/poco.drivers.android.uiautomation.html>`_
  - `cocos2dx-lua <source/poco.drivers.std.html>`_

..
 还没写完的连接先注释掉
 - `cocos2dx-js <source/poco.drivers.cocosjs.html>`_


Poco SDK API
''''''''''''

.. toctree::
    :maxdepth: 3

    Poco SDK API <source/poco.sdk>


.. toctree::
    :hidden:

    Examples and Tutorial <source/doc/poco-example/index>

.. toctree::
    :hidden:

    Project integration <source/doc/integration>


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


Join to discuss!
----------------




`join slack`_

.. _poco-sdk: source/doc/integration.html
.. _Integration Guide: source/doc/integration.html
.. _Integration Guide for NetEase: source/doc/integration.html#netease-internal-engines
.. _More examples: source/doc/poco-example/index.html
.. _Hunter内嵌inspector: source/doc/hunter-inspector-guide.html
.. _网易游戏项目测试脚本标准模板: source/doc/netease-internal-use-template.html
.. _android-native: http://poco.readthedocs.io/en/latest/source/doc/poco_for_android_native_app.html
.. _PocoUnit: https://github.com/AirtestProject/PocoUnit
.. _PocoHierarchyViewer: source/doc/about-standalone-inspector.html
.. _AirtestIDE: http://airtest.netease.com/

.. _join slack: https://join.slack.com/t/airtestproject/shared_invite/enQtMzYwMjc2NjQzNDkzLTcyMmJlNjgyNjgzZTRkNWRiYmE1YWI1ZWE5ZmQwYmM1YmY3ODZlMDc0YjkwMTQ5NDYxYmEyZWU1ZTFlZjg3ZjI
