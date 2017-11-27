
Basic Usage
===========

Wrap a pair of brackets after poco instance to select UI objects. The following example simply shows how to select a
button and perform a click.

.. code-block:: python

    # coding=utf-8

    from poco.drivers.unity3d import UnityPoco
    from airtest.core.api import connect_device


    connect_device('Android:///')
    poco = UnityPoco(('10.254.44.76', 5001))

    poco('btn_start').click()
