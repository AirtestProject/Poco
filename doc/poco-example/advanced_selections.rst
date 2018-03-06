
Advanced selections
===================

Selecting is very significant in specifying corresponding UI element in UI automated test. Under normal circumstances,
selecting by name is the simplest way. But in some cases the UI is not always named well, especially list-like
programmatically generated UI, which would not have a static name. Poco provides many powerful and effective ways to
select UI including by any existed attributes, hierarchy relationship and positional relationship. Most importantly,
any above ways can be chained or combined together to achieve more complicate selections.

[用例还需补充]

The following examples will show how to select UI in complicate scenes.

.. image:: img/g62-shop.png

.. code-block:: python

    # coding=utf-8

    from poco.drivers.unity3d import UnityPoco

    poco = UnityPoco()

    items = poco('main_node').child('list_item').offspring('name'):
    first_one = items[0]
    print(first_one.get_text())  # => '1/2活力药剂'
    first_one.click()

See also:

* `basic usage`_
* `interact with Buttons and Labels`_
* `drag and swipe operations`_
* `advanced selections`_
* `play with coordinate system and local positioning`_
* `iteration over elements`_
* `handling exceptions`_
* `waiting for events`_
* `play with unittest framework`_
* `optimize speed by freezing UI`_


.. _basic usage: basic.html
.. _interact with Buttons and Labels: interact_with_buttons_and_labels.html
.. _drag and swipe operations: drag_and_swipe_operations.html
.. _advanced selections: advanced_selections.html
.. _play with coordinate system and local positioning: play_with_coordinate_system_and_local_positioning.html
.. _iteration over elements: iteration_over_elements.html
.. _handling exceptions: handling_exceptions.html
.. _waiting for events: waiting_events.html
.. _play with unittest framework: play_with_unittest_framework.html
.. _optimize speed by freezing UI: optimize_speed_by_freezing_UI.html
