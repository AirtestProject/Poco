
Poco drivers (engine specific poco implementation)
==================================================

For different engines please initialize ``poco`` instance by corresponding driver. Here are API reference of different
drivers.

- `Unity3D`_
- `android-native`_
- `cocos2dx-js`_
- `NetEase Internal Engines`_

Following example shows how to initialize poco instance for Unity3D. Remember to connect an Android device to your
PC/mac with a running game or launch and keep the Unity game active on PC/mac.

.. code-block:: python

    # import unity poco driver from this path
    from poco.drivers.unity3d import UnityPoco

    # then initialize the poco instance in the following way
    poco = UnityPoco()

    # for windows
    # poco = UnityPoco(('localhost', 5001), unity_editor=True)

    # now you can play with poco
    ui = poco('...')
    ui.click()

For **cocos2dx-lua** games are similar as Unity3d drivers.

.. code-block:: python

    # import standard poco driver
    from poco.drivers.std import StdPoco
    from airtest.core.api import connect_device

    # connect a device first, then initialize poco object
    device = connect_device('Android:///')
    poco = StdPoco(10054, device)

    # now you can play with poco
    ui = poco('...')
    ui.click()

If multiple devices connected, please select one by invoking ``connect_device`` from airtest API.

.. code-block:: python

    from poco.drivers.unity3d import UnityPoco
    from airtest.core.api import connect_device

    connect_device('Android:///014E05DE0F02000E')  # connect device by serialno
    poco = UnityPoco()


For other engines, refer to `Integration guide`_ for more details

Device object
-------------

``Device`` is an abstract object which game/app runs on. In poco communicating with game/app is under a connection with
the device. This device connection is handled by `Airtest device abstraction`_ (take Android as example).

There are 2 ways to connect to the device.

* Call function `airtest.core.api.connect_device`_.
* Initialize Device instance according to platform (`android`_/`windows`_/`ios`_) then pass the device instance to Poco
  constructor according to different poco drivers.

.. _Integration Guide: integration.html
.. _Unity3D: ../poco.drivers.unity3d.unity3d_poco.html
.. _android-native: ../poco.drivers.android.uiautomation.html
.. _cocos2dx-js: ../poco.drivers.cocosjs.html
.. _NetEase Internal Engines: ../poco.drivers.netease.internal.html
.. _Airtest device abstraction: https://airtest.readthedocs.io/en/latest/all_module/airtest.core.android.android.html
.. _airtest.core.api.connect_device: https://airtest.readthedocs.io/en/latest/all_module/airtest.core.api.html#airtest.core.api.connect_device
.. _ios: https://airtest.readthedocs.io/en/latest/all_module/airtest.core.ios.ios.html
.. _android: https://airtest.readthedocs.io/en/latest/all_module/airtest.core.android.android.html
.. _windows: https://airtest.readthedocs.io/en/latest/all_module/airtest.core.win.win.html
