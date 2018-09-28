
MacOS app (poco driver)
=======================

This page will teach you how to use Poco to test your MacOS programs.
To test your program is very simple, just follow the steps below.

.. note::

    Only some GUI programs developed by Accessibility API are supported.
    For more information, please visit `Accessibility Programming Guide for OS X`_

.. Warning::

    Remember to give your script secure access. Specific steps are as follows.
    Navigate to ``System preferences`` -> ``Security and privacy`` -> ``privacy`` -> ``Accessibility``.
    Add your script access, usually is the terminal or your runtime environment


Dependency
----------

To run OSX Poco SDK, you need to install **Xcode first**, then install the following python libraries.

.. code-block:: bash

    pip install pyatomac pyautogui


Initialize a Poco instance
--------------------------

First you need to initialize a Poco instance. Remember to import the poco library first.
The first parameter is a dictionary that determines which window you want to test. 
The second parameter is an address that identifies the machine on which the program you are testing is located. 
The default is the local machine.

First, you have to decide which application the window you want to test is.There are three ways.

1. ``appname`` Find application by name. 
#. ``bundleid`` Find application by bundleid, something like "com.apple.Setting".
#. ``appname_re`` Find application by regular expression of name

Second, find the window you want to test in this application. There are three ways.

1. ``windowtitle`` Find window by name. 
#. ``windowindex`` Find window by window index.
#. ``windowtitle_re`` Find window by regular expression of name


You can use it by the following example

.. code-block:: python

    from poco.drivers.osx.osxui_poco import OSXPoco
    poco = OSXPoco({"appname": "Finder", "windowindex": 0})  # Find the first windows in 'Finder' application
    # poco = OSXPoco({"appname_re": "[a][b][c]", "windowtitle": "dirname"}, ("192.168.1.10", 15004))  # Find the window named 'dirname' by regular expression remotely
    # poco = OSXPoco({"bundleid": "com.apple.Finder", "windowtitle_re": "*.name"})


Poco also supports to **test multiple windows** at the same time. You only need to provide different addresses for
different poco instances.

.. Warning::

    If the parameters you provide cannot locate a unique window, an error will be reported. For example, a regular
    expressions as you provide may match multiple windows.

.. note::
    The osx driver has integrated the OSX SDK. If you are testing a local program, you can start the driver directly.
    If you are testing a remote program, you will need to launch the OSX SDK service on the remote machine.



Start testing your program
--------------------------

After initializing the poco instance, you can test your program.
Just like other engines, you can simulate various inputs of your device through Poco's own functions, such as
``click``, ``long_click``, ``swipe``, ``snapshot``. See `object proxy related operation`_ for more details.

Here simple examples.

.. code-block:: python

    from poco.drivers.osx.osxui_poco import OSXPoco
    poco = OSXPoco({"appname_re": "系统偏好", "windowindex": 0})
    poco("通用").click() 

.. note::

    If you don't know the name of the UI control in the window, you can check it out through our
    `Poco Hierarchy Viewer (UI Inspector)`_


.. _Accessibility Programming Guide for OS X: https://developer.apple.com/library/archive/documentation/Accessibility/Conceptual/AccessibilityMacOSX/index.html
.. _object proxy related operation: http://poco.readthedocs.io/en/latest/source/README.html#object-proxy-related-operation
.. _Poco Hierarchy Viewer (UI Inspector): https://poco.readthedocs.io/en/latest/source/doc/about-standalone-inspector.html
