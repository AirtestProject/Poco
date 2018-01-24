
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

The fish and bomb will come up from bottom right to left. Click the fish and avoid the bomb.

.. image:: img/wait_any_ui.gif

.. code-block:: python

    # coding=utf-8

    from poco.drivers.unity3d import UnityPoco
    from airtest.core.api import connect_device
    from poco.exceptions import PocoTargetTimeout


    connect_device('Android:///')
    poco = UnityPoco(('10.254.44.76', 5001))

    bomb_count = 0
    while True:
        blue_fish = poco('fish_emitter').child('blue')
        yellow_fish = poco('fish_emitter').child('yellow')
        bomb = poco('fish_emitter').child('bomb')
        fish = poco.wait_for_any([blue_fish, yellow_fish, bomb])
        if fish is bomb:
            # skip the bomb and count to 3 to exit
            bomb_count += 1
            if bomb_count > 3:
                return
        else:
            # otherwise click the fish to collect.
            fish.click()
        time.sleep(2.5)


The following example shows how to poll all of UIs in one time.

Wait until all 3 fishes appear on the screen.

.. image:: img/wait_all_ui.gif

.. code-block:: python

    # coding=utf-8

    import time
    from poco.drivers.unity3d import UnityPoco
    from airtest.core.api import connect_device


    connect_device('Android:///')
    poco = UnityPoco(('10.254.44.76', 5001))

    poco(text='wait UI 2').click()

    blue_fish = poco('fish_area').child('blue')
    yellow_fish = poco('fish_area').child('yellow')
    shark = poco('fish_area').child('black')

    poco.wait_for_all([blue_fish, yellow_fish, shark])
    poco('btn_back').click()
    time.sleep(2.5)

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
