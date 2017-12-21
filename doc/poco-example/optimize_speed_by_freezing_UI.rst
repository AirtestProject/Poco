
Optimize speed by freezing UI
=============================

This section introduces one of the way to speed up your test script only in complicate situations. For simple selection
and operations, you need not to do this optimization at all.

Freezing UI is just to dump the UI hierarchy and store it locally. With current hierarchy data, the position of UIs can
be retrieved directly without communicating with game/app which is slow if multiple visits. The only one disadvantage of
freezing UI is that the hierarchy data cannot stay in sync with game/app automatically. So you should handle your
UI state carefully otherwise you may get wired test results.

.. note::

    In some poco-sdk implementations, freezing and not freezing UI are equivalent. See poco engine specification for
    more details.

The following 2 examples shows the difference between freezing and not freezing UI.

使用netease的例子吧

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
