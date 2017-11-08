
How to integrate with PocoSDK
=============================

There are sdk implementations for some known game engines as follows.

If you find something stuck on integration, feel free to open an issue.

Unity
-----

1. Clone the sdk source code from `poco-sdk repo`_. 
#. Copy the ``Unity3D`` folder to your unity project script folder. You can rename the folder if you wish.
#. If you are using ``NGUI``, just remove the ugui sub folder. If you are using ``UGUI``, just remove the ngui sub 
   folder.
#. Attach the ``Unity3D/PocoManager.cs`` to the root ``gameObject`` or any new created one of your scene . Remember to 
   set ``never destroy`` flag on this ``gameObject``.

Not NGUI or UGUI ?
""""""""""""""""""

If your Unity3D project does not use NGUI or UGUI, you can still integrate poco-sdk and only some extra steps needed. 
See `implementation guide <implementation_guide.html>`_. This guide helps you implement the poco-sdk in your own type
of GUI. And also you can take a look at the source code in ``poco-sdk/Unity3D/NGUI`` which might make it more clear.

Cocos2dx-js
-----------

The major version of cocos2dx should >= 3. Poco-sdk js version is compatible with ES5.

1. Clone the sdk source code from `poco-sdk repo`_. 
#. Copy the ``cocos2dx-js`` folder to your project script folder. You can rename the folder if you wish.
#. **Extra Step**: build the socket/websocket module?
#. Initialize poco-sdk by copying following code to your game initialization script.

.. code-block:: javascript

    var poco = require('poco-manager')
    // ???


Cocos2dx-lua
------------

The major version of cocos2dx should >= 3.

1. Clone the sdk source code from `poco-sdk repo`_. 
#. Copy the ``cocos2dx-lua`` folder to your project script folder. You can rename the folder if you wish.
#. **Extra Step**: build the socket/websocket module?
#. Initialize poco-sdk by copying following code to your game initialization script.

.. code-block:: lua

    local poco = require('poco-manager')
    -- ???

Unreal
------

(coming soon.)

Android Native App
------------------

It is not necessary to integrate poco-sdk to the app. Just simply write the test code and be happy with it.
See `poco for Android Native App`_ section for more details.


Other engines
-------------

See `implementation guide <implementation_guide.html>`_. This guide helps you implement and integrate poco-sdk with 
your app step by step.

.. _poco-sdk repo: https://github.com/Meteorix/poco-sdk
.. _poco for Android Native App: 
