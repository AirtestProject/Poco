
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
#. **Extra Step**: build the socket/websocket module?
#. ``require('poco-manager')``  in your game's first initialized script to start PocoSDK.

.. code-block:: javascript

    var poco = require('poco-manager')
    // ...


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

Already ready for using. No need to do anything!

Other Engines
-------------

See `implementation guide <implementation_guide.html>`_. This guide helps you implement and integrate PocoSDK with your game step by step.

.. _poco-sdk repo: https://github.com/Meteorix/poco-sdk
.. _poco for Android Native App:
