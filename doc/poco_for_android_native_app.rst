
Poco for Android Native App
===========================

Poco also supports to write tests for Android native apps. It is an alternative framework for `xiaocong/uiautomator`_
and its APIs are more powerful and easy to use. You don't need to setup an AndroidSDK environment and other dependencies.
Only adb tools are required. Just simply install poco with following command.

.. code-block:: bash

    pip install pocoui

The following example shows how to start writing test scripts. Remember to connect an Android device to your PC/mac
first and enable the **ADB DEBUG MODE**.

.. code-block:: python

    from poco.drivers.android.uiautomation import AndroidUiautomationPoco

    poco = AndroidUiautomationPoco()
    poco.device.wake()
    poco(text='Clock').click()


If multiple devices are connected, simply invoke airtest ``connect_device``.

.. code-block:: python

    from poco.drivers.android.uiautomation import AndroidUiautomationPoco
    from airtest.core.api import connect_device

    connect_device('Android://014E05DE0F02000E/')  # connect device first by serialno.

    poco = AndroidUiautomationPoco()
    poco.device.wake()

If you want to control multiple devices at one time, see the following example.

.. code-block:: python

    from poco.drivers.android.uiautomation import AndroidUiautomationPoco
    from airtest.core.android import Android

    # initialize 2 device objects
    dev1 = Android('014E05DE0F02000E')
    dev2 = Android('0123456789')

    poco1 = AndroidUiautomationPoco(dev1)
    poco2 = AndroidUiautomationPoco(dev2)
    poco1.device.wake()
    poco2.device.wake()

More usage are similar to poco drivers for other game engines. Use `PocoHierarchyViewer`_ to retrieve the view structure.

.. _xiaocong/uiautomator: https://github.com/xiaocong/uiautomator
.. _PocoHierarchyViewer: doc/about-standalone-inspector.html
