
Play with coordinate system and local positioning
=================================================

In poco, coordinates are always normalized from 0 to 1. You can simply think of it the percentage size and positions.
In case that you need to interact with UI nearby or just want to click the button's edge rather than the center, you
can use local positioning by specifying a offset.

In general, to interact with UI always starts with a point, such as click or drag from the point. Local positioning
allows you to make any offset from the selected UI without selecting another UI.

.. image:: ../img/hunter-poco-coordinate-system.png

The following examples will show how to click different point inside selected UI.

.. code-block:: python

    # coding=utf-8

    from poco.drivers.unity3d import UnityPoco
    from airtest.core.api import connect_device


    connect_device('Android:///')
    poco = UnityPoco(('10.254.44.76', 5001))

    # click the logo
    logo = poco('logo')
    logo.focus('center').click()
    logo.focus([0.5, 0.5]).click()  # the same as 'center'
    logo.focus([0, 0]).click()  # top left corner
    logo.focus([1, 1]).click()  # bottom down corner

    # drag the star
    star = poco('star')
    star.focus('center').swipe(direction=[0.1, 0])  # from 'center' towards right
    star.focus([0, 0]).swipe(dirextion=[0.1, 0])  # from 'top left' towards right

Can also click outside the selected UI. It is very useful to click some models by its name tag.

来个梦幻人物脚底下名字的截图

.. code-block:: python

    # coding=utf-8

    npc_name = poco(text='袁天罡')
    npc = npc_name.focus([0.5, -1])
    npc.click()

The following examples show that ``focus`` is an immutable method that will not impact the origin UI.

.. code-block:: python

    # focus is immutable
    button = poco('button')
    button_right_edge = button.focus([1, 0.5])
    button.click()  # still click the center
    button_right_edge.click()  # will click the right edge

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
