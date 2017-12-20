
Drag and Swipe operations
=========================

Like click, drag and swipe are other types of actions on UI. Drag usually starts from and ends to specific UI, but
Swipe can be performed from any point to any point.

The following example shows how to swipe or drag from A to B.

.. code-block:: python

    # coding=utf-8

    from poco.drivers.unity3d import UnityPoco
    from airtest.core.api import connect_device


    connect_device('Android:///')
    poco = UnityPoco(('10.254.44.76', 5001))


    # drag the "star" to the "shell"
    poco('star').drag_to(poco('shell'))

    # swipe the list view up
    poco(type='ListView').swipe([0, -0.1])
    poco(type='ListView').swipe('up')  # the same as above, also have down/left/right

    # perform swipe without UI selected
    x, y = poco(type='ListView').get_position()
    end = [x, y - 0.1]
    dir = [0, -0.1]
    poco.swipe([x, y], end)  # drag from point A to point B
    poco.swipe([x, y], direction=dir)  # drag from point A toward given direction and length
