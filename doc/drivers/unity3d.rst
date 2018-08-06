
Unity3D (poco driver)
=====================

Following example shows how to initialize poco instance for Unity3D games on Windows, UnityEditor or Android.

Android (default)
-----------------

Remember to connect an Android device to your PC/mac with a running game.

.. code-block:: python

    # import unity poco driver from this path
    from poco.drivers.unity3d import UnityPoco

    # then initialize the poco instance in the following way
    poco = UnityPoco()

    # now you can play with poco
    ui = poco('...')
    ui.click()

If multiple devices connected to your PC/mac, please select the device in the following way.

.. code-block:: python

    # import unity poco driver from this path
    from poco.drivers.unity3d import UnityPoco
    from airtest.core.api import connect_device

    # select one of your android device first by given serialno
    dev = connect_device('Android:///<serialno>')

    # make sure your poco-sdk in the game runtime listens on the following port.
    # default value will be 5001
    # IP is not used for now
    addr = ('', 5001)

    # then initialize the poco instance in the following way
    # specifying the device object
    poco = UnityPoco(addr, device=dev)

    # now you can play with poco
    ui = poco('...')
    ui.click()

Unity player on Windows
-----------------------

Similar to Android, if the game runs on Windows, simply connect to the window device in the following way.
The only difference is on ``connect_device``. More window selectors refer to `airtest.core.api.connect_device`_.

.. code-block:: python

    # import unity poco driver from this path
    from poco.drivers.unity3d import UnityPoco
    from airtest.core.api import connect_device

    # select the window object by title regex
    dev = connect_device('Windows:///?title_re=^your game title.*$')

    # make sure your poco-sdk in the game runtime listens on the following port.
    # default value will be 5001
    # IP is not used for now
    addr = ('', 5001)

    # then initialize the poco instance in the following way
    # specifying the device object
    poco = UnityPoco(addr, device=dev)

    # now you can play with poco
    ui = poco('...')
    ui.click()


UnityEditor on Windows
----------------------

Poco driver is also available for UnityEditor, which is easy for game debugging. Use ``UnityEditorWindow`` to initialize
the device object will do.

.. code-block:: python

    # import unity poco driver from this path
    from poco.drivers.unity3d import UnityPoco
    from poco.drivers.unity3d.device import UnityEditorWindow

    # specify to work on UnityEditor in this way
    dev = UnityEditorWindow()

    # make sure your poco-sdk component listens on the following port.
    # default value will be 5001. change to any other if your like.
    # IP is not used for now
    addr = ('', 5001)

    # then initialize the poco instance in the following way
    # specifying the device object
    poco = UnityPoco(addr, device=dev)

    # now you can play with poco
    ui = poco('...')
    ui.click()


Multiple devices together (mixed platforms)
-------------------------------------------

If you are going to control multiple devices in the same test case, please follow the following example.

.. code-block:: python

    # import unity poco driver from this path
    from poco.drivers.unity3d import UnityPoco
    from poco.drivers.unity3d.device import UnityEditorWindow

    # initialize different device object one by one
    dev1 = UnityEditorWindow()
    dev2 = connect_device('Android:///')
    dev3 = connect_device('Windows:///?title_re=^title xxx.*$')

    # use this default address. separate them if the devices do not listens on the same port.
    addr = ('', 5001)

    # initialize poco instance one by one by specifying different device object
    poco1 = UnityPoco(addr, device=dev1)
    poco2 = UnityPoco(addr, device=dev2)
    poco3 = UnityPoco(addr, device=dev3)

    # now you can play with poco
    ui1 = poco1('...')
    ui1.click()
    ui2 = poco2('...')
    ui2.swipe('up')


.. _airtest.core.api.connect_device: https://airtest.readthedocs.io/en/latest/all_module/airtest.core.api.html#airtest.core.api.connect_device