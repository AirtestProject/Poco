
Waiting for events
==================

Interact with UI without feedback will be pretty hard in some cases, especially you are waiting for some events,
notifications or state changing on UIs. Poco provides simple poll mechanism to allow you to poll some events of UIs.
This section will show how to stay in sync with UIs and poll for state changing.

The following example shows the simplest way to stay in sync with UIs.

.. code-block:: python

    # coding=utf-8

    from poco.drivers.unity3d import UnityPoco
    from airtest.core.api import connect_device


    connect_device('Android:///')
    poco = UnityPoco(('10.254.44.76', 5001))

    # start and waiting for switching scene
    start_btn = poco('start')
    start_btn.click()
    start_btn.wait_for_disappearance()

    # waiting for the scene ready then click
    exit_btn = poco('exit')
    exit_btn.wait_for_appearance()
    exit_btn.click()

The following example shows how to poll any of UIs in one time.

.. code-block:: python

    # coding=utf-8

    from poco.drivers.unity3d import UnityPoco
    from airtest.core.api import connect_device
    from poco.exceptions import PocoTargetTimeout


    connect_device('Android:///')
    poco = UnityPoco(('10.254.44.76', 5001))

    shell = poco('shell')
    basket = poco('basket')
    while True:
        star = poco('start')
        fish = poco('fish')

        try:
            result = poco.wait_for_any([star, fish])
        except PocoTargetTimeout:
            # if no more fish or star within timeout
            break

        if result is star:
            result.drag_to(shell)  # star to shell
        elif result is fish:
            result.drag_to(basket)  # fish to basket


The following example shows how to poll all of UIs in one time.

.. code-block:: python

    # coding=utf-8

    from poco.drivers.unity3d import UnityPoco
    from airtest.core.api import connect_device
    from poco.exceptions import PocoTargetTimeout


    connect_device('Android:///')
    poco = UnityPoco(('10.254.44.76', 5001))

    shell = poco('shell')
    star = poco('star')

    try:
        poco.wait_for_all([star, shell])
    except PocoTargetTimeout:
        print('oops!')
        raise
    star.drag_to(shell)

See also:

* `basic usage`_
* `interact with Buttons and Labels`_
* `drag and swipe operations`_
* `advanced selections`_
* `play with coordinate system and local positioning`_
* `iteration over elements`_
* `handling exceptions`_
* `waiting events`_
* `play with unittest framework`_
* `optimize speed by freezing UI`_


.. _basic usage: basic.html
.. _interact with Buttons and Labels: interact_with_buttons_and_labels.html
.. _drag and swipe operations: drag_and_swipe_operations.html
.. _advanced selections: advanced_selections.html
.. _play with coordinate system and local positioning: play_with_coordinate_system_and_local_positioning.html
.. _iteration over elements: iteration_over_elements.html
.. _handling exceptions: handling_exceptions.html
.. _waiting events: waiting_events.html
.. _play with unittest framework: play_with_unittest_framework.html
.. _optimize speed by freezing UI: optimize_speed_by_freezing_UI.html
