
cocos2dx-lua (poco driver)
==========================

Following example shows how to initialize poco instance for cocos2dx-lua games on Android.

Android (default)
-----------------

Remember to connect an Android device to your PC/mac with a running game.

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

