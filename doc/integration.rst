
PocoSDK Integration Guide
=========================

PocoSDK implementations for most popular game engines are already provided in `poco-sdk repo`_. You can easily integrate PocoSDK in your game following the corresponding instruction.

Feel free to open an issue if you get stuck in integration.

Unity3D
-------
PocoSDK supports Unity3D version 4 & 5, ngui & ugui, C# only for now. If your game is not supported yet, please refer to `implementation guide <implementation_guide.html>`_.

1. Clone source code from `poco-sdk repo`_. 
#. Copy the ``Unity3D`` folder to your unity project script folder.
#. If you are using ``ngui``, just remove the sub folder ``Unity3D/ugui`` . If you are using ``ugui``, just remove the sub folder ``Unity3D/ngui`` .
#. Add ``Unity3D/PocoManager.cs`` as script component on any permanent ``GameObject`` that will never be destroyed during game's lifetime.


Cocos2dx-js
-----------

PocoSDK supports Cocos2dx version >= 3.0. To support cocos-js games on Android, the javascript sdk is implemented in ES5.

1. Clone sdk source code from `poco-sdk repo`_. 
#. Copy the ``cocos2dx-js`` folder to your cocos project script folder.
#. Build websocket server module and js bindings for RPC server use, `websocketserver reference`_.
    #. ``cp -r cocos2dx-js/3rd/websockets <your-cocos-project>/build/jsb-default/frameworks/cocos2d-x/external/websockets``
    #. ``cp cocos2dx-js/3rd/src/* <your-cocos-project>/build/jsb-default/frameworks/cocos2d-x/runtime-src/Classes``
    *. edit ``<your-cocos-project>/build/jsb-default/frameworks/cocos2d-x/runtime-src/Classes/AppDelegate.cpp``
        add line ``#include "jsb_websocketserver.h"``
        add line ``sc->addRegisterCallback(register_jsb_websocketserver);`` in the middle of file after ``#if (CC_TARGET_PLATFORM == CC_PLATFORM_ANDROID)``
    *. edit ``<your-cocos-project>/build/jsb-default/frameworks/cocos2d-x/runtime-src/proj.android/jni/Android.mk``
        add ``LOCAL_SRC_FILES := ../../Classes/WebSocketServer.cpp ../../Classes/jsb_websocketserver.cpp``
        add ``LOCAL_STATIC_LIBRARIES := websockets_static``
    #. recompile your cocos project
#. ``require('Poco')``  in your game's first initialized script to start PocoSDK, and do not destroy it during game's lifetime.

.. code-block:: javascript

    var PocoManager = require('Poco')
    var poco = new PocoManager()

    // add poco on window object to persist
    window.poco = poco


Cocos2dx-lua
------------

PocoSDK supports Cocos2dx version >= 3.0. 

1. Clone the sdk source code from `poco-sdk repo`_. 
#. Copy the ``cocos2dx-lua`` folder to your project script folder. You can rename the folder if you wish.
#. **Extra Step**: build the socket/websocket module?
#. Initialize poco-sdk by copying following code to your game initialization script.

.. code-block:: lua

    local poco = require('poco-manager')
    -- ...

Unreal
------

(Coming soon.)

Android Native App
------------------

Nothing to do about integration. Just start writing tests and be happy.
See `poco for Android Native App`_ section for more details.

Netease Internal Engines
------------------------

Just config the module preload at `Hunter`_. Please append following script to the end of hunter ``__init__``
instruction. Require safaia version >= 1.2.0. Use ``print Safaia.__version__`` to get current version.
Any questions about hunter feel free to contact ``lxn3032@corp.netease.com``.

* for NeoX

.. code-block:: python

    # poco uiautomation
    PocoUiautomation = require('support.poco.neox.uiautomation')
    Safaia().install(PocoUiautomation)

    # inspector extension
    screen_handler = require('support.poco.neox.screen')()
    InspectorExt = require('support.poco.safaia.inspector')
    InspectorExt.screen = screen_handler
    InspectorExt.dumper = require('support.poco.neox.Dumper')()
    Safaia().install(InspectorExt)

* for Messiah

.. code-block:: python

    # poco uiautomation
    PocoUiautomation = require('support.poco.messiah.uiautomation')
    Safaia().install(PocoUiautomation)

    # inspector extension
    screen_handler = require('support.poco.messiah.screen')()
    InspectorExt = require('support.poco.safaia.inspector')
    InspectorExt.screen = screen_handler
    InspectorExt.dumper = require('support.poco.cocos2dx.Dumper')()
    Safaia().install(InspectorExt)

* for cocos2dx-* and others: please contact ``lxn3032@corp.netease.com``.

Other Engines
-------------

See `implementation guide <implementation_guide.html>`_. This guide helps you implement and integrate PocoSDK with your game step by step.

.. _poco-sdk repo: https://github.com/AirtestProject/Poco-SDK
.. _poco for Android Native App: poco_for_android_native_app.html
.. _Hunter: http://hunter.nie.netease.com/mywork/instruction
.. _websocketserver reference: http://discuss.cocos2d-x.org/t/cocos2d-js-websocket-server/33570