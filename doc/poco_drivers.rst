
Poco drivers (engine specific poco implementation)
==================================================

For different engines please initialize ``poco`` instance by corresponding driver. Here are API reference of different
drivers.

- `Unity3D`_
- `android-native`_
- `cocos2dx-js`_
- `NetEase Internal Engines`_

Following example shows how to initialize popo instance for Unity3D. Remember to connect an Android device to your
PC/mac with a running game or launch and keep the Unity game active on PC/mac.

.. code-block:: python

    # import unity poco driver from this path
    from poco.drivers.unity3d import UnityPoco
    from airtest.core.api import connect_device

    # then initialize the poco instance in the following way
    poco = UnityPoco()

    # for windows
    # poco = UnityPoco(('localhost', 5001), unity_editor=True)

    # now you can play with poco
    ui = poco('...')
    ui.click()

If multiple devices connected, please select one by invoke ``connect_device`` from airtest API.

.. code-block:: python

    from poco.drivers.unity3d import UnityPoco
    from airtest.core.api import connect_device

    connect_device('Android://014E05DE0F02000E/')  # connect device by serialno
    poco = UnityPoco()


For other engines, refer to `Integration guide`_ for more details

.. _Integration Guide: integration.html
.. _Unity3D: ../poco.drivers.unity3d.unity3d_poco.html
.. _android-native: ../poco.drivers.android.uiautomation.html
.. _cocos2dx-js: ../poco.drivers.cocosjs.html
.. _NetEase Internal Engines: ../poco.drivers.netease.internal.html
