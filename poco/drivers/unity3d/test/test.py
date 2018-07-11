# coding=utf-8

import base64
import json
import traceback
import time
import unittest

from poco.drivers.std.test.simple import TestStandardFunction
from poco.drivers.unity3d.unity3d_poco import UnityPoco
from airtest.core.api import connect_device


class TestU3dDriverAndroid(TestStandardFunction):
    @classmethod
    def setUpClass(cls):
        connect_device('Android:///')
        cls.poco = UnityPoco()


class TestU3dDriverUnityEditor(TestStandardFunction):
    @classmethod
    def setUpClass(cls):
        cls.poco = UnityPoco(unity_editor=True)


if __name__ == '__main__':
    unittest.main()
