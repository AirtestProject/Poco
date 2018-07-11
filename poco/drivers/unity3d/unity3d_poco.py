# -*- coding: utf-8 -*-
# @Author: gzliuxin
# @Email:  gzliuxin@corp.netease.com
# @Date:   2017-07-14 19:47:51

from poco.drivers.std import StdPoco

from airtest.core.api import connect_device, device as current_device


__all__ = ['UnityPoco']
DEFAULT_PORT = 5001
DEFAULT_ADDR = ("localhost", DEFAULT_PORT)


class UnityPoco(StdPoco):
    """
    Poco Unity3D implementation.

    Args:
        addr (:py:obj:`tuple`): the endpoint of your Unity3D game, default to ``("localhost", 5001)``
        unity_editor (:py:obj:`bool`): whether your Unity3D game is running in UnityEditor or not. default to ``False``
        connect_default_device (:py:obj:`bool`): whether connect to a default device if no devices selected manually.
         default to ``True``.
        options: see :py:class:`poco.pocofw.Poco`

    Examples:
        If your game is running on Android, you could initialize poco instance by using following snippet::
            
            from poco.drivers.unity3d import UnityPoco
            
            # your phone and your PC/mac should be inside the same sub-net.
            ip = '<ip address of your phone>'
            poco = UnityPoco((ip, 5001))
            poco('button').click()
            ...

    """

    def __init__(self, addr=DEFAULT_ADDR, unity_editor=False, connect_default_device=True, **options):
        if 'action_interval' not in options:
            options['action_interval'] = 0.5

        dev = None
        if unity_editor:
            dev = connect_device("Windows:///?class_name=UnityContainerWndClass&title_re=Unity.*")
            game_window = dev.app.top_window().child_window(title="UnityEditor.GameView")
            dev._top_window = game_window.wrapper_object()
            dev.focus_rect = (0, 40, 0, 0)

        if connect_default_device and not current_device():
            # currently only connect to Android as default
            # can apply auto detection in the future
            dev = connect_device("Android:///")

        super(UnityPoco, self).__init__(addr[1], dev, **options)
