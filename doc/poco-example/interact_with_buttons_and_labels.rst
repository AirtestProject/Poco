
Interact with Buttons and Labels
================================

UI objects are just proxies, you can assign it into a variable and reuse without repeated instantiation. The following
example shows the most used methods of UI proxy. It is very easy to access all available attributes of UI in game/app.

If retrieve attributes or perform an operation on inexistent UI, exceptions will raise. If you are not sure whether
the UI exists or not, you can call ``.exists()`` to test whether exists. In specific test cases, remember to think of
a bug if the UI does not exist as your wish.

.. code-block:: python

    # coding=utf-8

    from poco.drivers.unity3d import UnityPoco
    from airtest.core.api import connect_device


    connect_device('Android:///')
    poco = UnityPoco(('10.254.44.76', 5001))

    btn = poco('btn_start')
    btn.click()
    print(btn.get_text())  # => 'Start'

    intro = poco('introduction')
    print(intro.get_text())  # => 'xxxx'
    print(intro.attr('text'))  # => 'xxxx'
    print(intro.attr('type'))  # => 'Text'
    print(intro.attr('texture'))  # => None. Because there is no texture on Text.
    print(intro.attr('foo-bar'))  # => None. Because "intro" dose not have an attribute named "foo-bar".

    intro.click()  # Perform a click on any UI objects are allowed.

    obj = poco('foo-bar', type='FooBar')
    print(obj.exists())  # => False. This UI does not exist actually

    invisible_obj = poco('result_panel', type='Layer')
    print(invisible_obj.exists())  # => False. This UI is not visible to user.

