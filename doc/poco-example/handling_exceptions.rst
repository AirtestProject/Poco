
Handling exceptions
===================

In poco, there are only 4 exceptions should care about. For other exceptions such RuntimeError, consider as a bug in
your test script. If you think it is poco's bug, feel free to open an issue.

:py:class:`InvalidOperationException <poco.exceptions.InvalidOperationException>`
---------------------------------------------------------------------------------

If the operation you performed takes no effects or unable to complete, you will get this exception.
If you got this exception, you should check your script carefully. Mostly because the UI you selected is outside the
screen and a operation performed on it. See the following example.

.. code-block:: python

    # coding=utf-8

    from poco.drivers.unity3d import UnityPoco
    from airtest.core.api import connect_device
    from poco.exceptions import InvalidOperationException


    connect_device('Android:///')
    poco = UnityPoco(('10.254.44.76', 5001))

    try:
        poco.click([1.1, 1.1])  # click outside screen
    except InvalidOperationException:
        print('oops')



:py:class:`PocoNoSuchNodeException <poco.exceptions.PocoNoSuchNodeException>`
-----------------------------------------------------------------------------

If read attributes from or perform operations on UI that is not actually exists, you will get this exception.
You can simply test whether the node exists or not by invoke ``.exists()``.

.. note::

    - Selecting any UI any store it without doing anything on it will never get exceptions. As the selected UI is only
      a UI proxy which represents the UI object in the game/app.
    - If a UI that is transparent and you cannot see it, it should be considered as existence. And also you can perform
      any operations on it.

.. code-block:: python

    # coding=utf-8

    from poco.drivers.unity3d import UnityPoco
    from airtest.core.api import connect_device
    from poco.exceptions import PocoNoSuchNodeException


    connect_device('Android:///')
    poco = UnityPoco(('10.254.44.76', 5001))

    node = poco('not existed node')  # select will never raise any exceptions
    try:
        node.click()
    except PocoNoSuchNodeException:
        print('oops!')

    try:
        node.attr('text')
    except PocoNoSuchNodeException:
        print('oops!')

    print(node.exists())  # => False. this method will not raise


:py:class:`PocoTargetTimeout <poco.exceptions.PocoTargetTimeout>`
-----------------------------------------------------------------

This exception only raises when you are waiting some conditions. Such as waiting the UI to appear or disappear.
It is quite different from ``PocoNoSuchNodeException``. If your operation is too fast that the UI is not keep up on
the screen, you will probably get ``PocoNoSuchNodeException`` rather than ``PocoTargetTimeout``.

The following example shows how to deal with this situation and stay in sync with the UI.

.. code-block:: python

    # coding=utf-8

    from poco.drivers.unity3d import UnityPoco
    from airtest.core.api import connect_device
    from poco.exceptions import PocoTargetTimeout


    connect_device('Android:///')
    poco = UnityPoco(('10.254.44.76', 5001))

    # UI is very slow
    poco('start').click()
    exit_btn = poco('exit')
    try:
        exit_btn.wait_for_appearance(timeout=10)  # wait until appearance within 10s
    except PocoTargetTimeout:
        print('oops!')
    else:
        exit_btn.click()


:py:class:`PocoTargetRemovedException <poco.exceptions.PocoTargetRemovedException>`
-----------------------------------------------------------------------------------

Unlike the above, if your operations are much slower than the UI, you may probably get this exceptions. This exception
seldom raises under normal circumstances. If you see this exception mostly because the UI you performed operation
on has already removed from the game/app.

The following example shows clicking on a no longer valid UI.

.. code-block:: python

    # coding=utf-8

    from poco.exceptions import PocoTargetRemovedException, PocoNoSuchNodeException


    poco = Poco(...)

    start = poco('start')
    print(start.exists())  # => True.
    start.click()
    print(start.exists())  # => False
    try:
        start.click()
    except PocoTargetRemovedException:
        print('oops!')

    # IMPORTANT NOTE:
    # `start2` is different from `start` !
    # `start` is tracking the UI at initial and it knows itself was removed but `start2`
    # does not know anything before.
    start2 = poco('start')
    try:
        start2.click()
    except PocoNoSuchNodeException:
        print('oops!')

.. note::

    In some poco-sdk implementations, this exceptions is never raised. So please test existence state carefully by
    your own when using previously defined UI proxies. See the following example.

.. code-block:: python

    # coding=utf-8

    from poco.drivers.unity3d import UnityPoco
    from airtest.core.api import connect_device


    connect_device('Android:///')
    poco = UnityPoco(('10.254.44.76', 5001))

    # no PocoTargetRemovedException case
    start = poco('start')
    print(start.exists())  # => True.
    start.click()
    print(start.exists())  # => False

    # IMPORTANT: In Unity3d, this operation will click the same coordinate as previous
    # and no matter what actually happens
    start.click()

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
