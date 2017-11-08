
How to integrate with PocoSDK
=============================

There are sdk implementations for some known game engines as follows.

If you find something stuck on integration, feel free to open an issue.

Unity
-----

1. Clone the sdk source code from `poco-sdk repo`_. 
#. Copy the Unity3D folder to your unity project script folder. You can rename the folder if you like.
#. If you are using ``NGUI``, just remove the ugui sub folder. If you are using ``UGUI``, just remove the ngui sub 
   folder.
#. Attach the ``Unity3D/PocoManager.cs`` to the root ``gameObject`` or any new created one of your scene . Remember to 
   set ``never destroy`` flag on this ``gameObject``.

Not NGUI or UGUI ?
""""""""""""""""""

See `implementation guide <implementation_guide.html>`_. This guide helps you implement the poco-sdk in your own type
of GUI. And also you can take a look at the source code in ``poco-sdk/Unity3D/NGUI`` which might make it more clear.

Cocos2dx
--------

The major version of cocos2dx should >= 3. Poco-sdk js version is compatible with ES5.

1. Clone the sdk source code from `poco-sdk repo`_. 
#. For different script language, copy corresponding folder to your project script folder. You can rename the folder if 
   you like.

    - js: cocos2dx-js 
    - lua: cocos2dx-lua 

#. Initialize poco-sdk by copy following code to your game initialization script.

For js:

.. code-block:: javascript

    var poco = require('poco-manager')
    // ???

For lua:

.. code-block:: lua

    local poco = require('poco-manager')
    -- ???

Other engines
-------------

See `implementation guide <implementation_guide.html>`_. This guide helps you implement and integrate poco-sdk with 
your app step by step.

.. _poco-sdk repo: https://github.com/Meteorix/poco-sdk
