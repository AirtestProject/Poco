# -*- coding: utf-8 -*-
# @Author: gzliuxin
# @Email:  gzliuxin@corp.netease.com
# @Date:   2017-07-14 19:47:51

from poco.drivers.std import StdPoco
from poco.drivers.unity3d.device import UnityEditorWindow
from poco.exceptions import InvalidOperationException
from airtest.core.api import connect_device, device as current_device

__all__ = ['UnityPoco']
DEFAULT_PORT = 5001
DEFAULT_ADDR = ("localhost", DEFAULT_PORT)


class UnityVRSupport():
    def __init__(self, client):
        self.client = client
        self.support_vr = False
        try:
            self.support_vr = self.client.call("isVrSupported")
        except InvalidOperationException:
            raise InvalidOperationException('VR not supported')

    def hasMovementFinished(self):
        success, error_msg  =self.client.call("hasMovementFinished").wait()
        print(success)
        if success != None:
            return True
        else:
            return False

    def rotateObject(self, x, y, z, camera, follower, speed=0.125):
        return self.client.call("RotateObject", x, y, z, camera, follower, speed)

    def objectLookAt(self, name, camera, follower, speed=0.125):
        return self.client.call("ObjectLookAt", name, camera, follower, speed)


class UnityPoco(StdPoco):
    """
    Poco Unity3D implementation.

    Args:
        addr (:py:obj:`tuple`): the endpoint of your Unity3D game, default to ``("localhost", 5001)``
        unity_editor (:py:obj:`bool`): whether your Unity3D game is running in UnityEditor or not. default to ``False``
        connect_default_device (:py:obj:`bool`): whether connect to a default device if no devices selected manually.
         default to ``True``.
         device (:py:obj:`Device`): :py:obj:`airtest.core.device.Device` instance provided by ``airtest``. leave the
         parameter default and the default device will be chosen. more details refer to ``airtest doc``
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

    def __init__(self, addr=DEFAULT_ADDR, unity_editor=False, connect_default_device=True, device=None, **options):
        if 'action_interval' not in options:
            options['action_interval'] = 0.5

        if unity_editor:
            dev = UnityEditorWindow()
        else:
            dev = device or current_device()

        if dev is None and connect_default_device and not current_device():
            # currently only connect to Android as default
            # can apply auto detection in the future
            dev = connect_device("Android:///")

        super(UnityPoco, self).__init__(addr[1], dev, ip=addr[0], **options)
        # If some devices fail to initialize, the UI tree cannot be obtained
        # self.vr = UnityVRSupport(self.agent.rpc)

    def send_message(self, message):
        self.agent.rpc.call("SendMessage", message)

    def invoke(self, listener, **kwargs):
        callback = self.agent.rpc.call("Invoke", listener=listener, data=kwargs)

        value, error = callback.wait()

        if error is not None:
            raise Exception(error)

        return value
