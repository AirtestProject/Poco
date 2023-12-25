
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


Integrating and Using Poco Interface Functions in Unity
-------------------------------------------------------

This document serves as a guide for integrating and using the new ``UnityPoco.sendMessage()`` and ``UnityPoco.invoke()`` functions in your Unity project.
These functions facilitate communication between your Unity game and Poco, allowing for simple calls with single string arguments or calls with custom arguments.

Getting Started
````````````````

Before using the new interfaces, ensure that you have the latest version of the Poco SDK that includes the changelog updates mentioned. This functionality relies on the updates provided in https://github.com/AirtestProject/Poco-SDK/pull/123.

Using the ``sendMessage()`` Function
`````````````````````````````````````

The ``UnityPoco.sendMessage()`` function allows you to send simple messages with a single string argument from Poco to Unity.

Unity-side
~~~~~~~~~~

Implement OnPocoMessageReceived and add it to PocoManager.MessageReceived. This function will be called when a message is received from Poco.

.. code-block:: csharp

    PocoManager.MessageReceived += OnPocoMessageReceived;


Poco-side
~~~~~~~~~

To use the ``sendMessage()`` function on the Poco side, you just need to call it and pass the message.

.. code-block:: python

    poco = UnityPoco()
    poco.sendMessage("Your message here")



Using the ``invoke()`` Function
```````````````````````````````

The ``UnityPoco.invoke()`` function allows for more complex interactions with custom arguments.

Poco-side
~~~~~~~~~

To use the ``invoke()`` function on the Poco side, you'll need to specify the listener and the arguments you want to pass.

.. code-block:: python

    poco = UnityPoco()
    poco.invoke(listener="say_hello", name="anonymous", year=2024)

Unity-side
~~~~~~~~~~

On the Unity side, set up a method that will be called when ``invoke()`` is used from Poco.

1. Create a class that derives from ``PocoListenerBase``.
2. Add a method that corresponds to the ``invoke()`` call:

   .. code-block:: csharp

       [PocoMethod("say_hello")]
       public void SayHello(string name, int year)
       {
           Debug.Log($"Hi, {name}! The year {year} is coming soon!");
       }

3. Add a reference to the new class in the ``PocoManager`` so that it knows to listen for calls to the ``say_hello`` method.

.. _airtest.core.api.connect_device: https://airtest.readthedocs.io/en/latest/all_module/airtest.core.api.html#airtest.core.api.connect_device