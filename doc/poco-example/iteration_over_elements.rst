
Iteration over elements
=======================

Poco provides the easiest way to interact with a serials of UI. That is to iterate over the selected UIs via for-loop.
In the loop, the iterator is also the the UI proxy. You can apply any method just like other selected UI.

The following example shows how to buy all merchandises on the current screen.

.. image:: img/g62-shop.png

.. code-block:: python

    # coding=utf-8

    from poco.drivers.unity3d import UnityPoco
    from airtest.core.api import connect_device


    connect_device('Android:///')
    poco = UnityPoco(('10.254.44.76', 5001))

    bought_items = set()
    for item in self.poco('main_node').child('list_item').offspring('name'):
        item_name = item.get_text()

        # markdown the bought item
        if item_name not in bought_items:
            item.click()
            bought_items.add(item_name)

