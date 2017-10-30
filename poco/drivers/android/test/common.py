# coding=utf-8


import time
import base64
import unittest

from poco.drivers.android.uiautomation import AndroidUiautomationPoco
from airtest.core.android import Android


class TestCommonCases(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.poco = AndroidUiautomationPoco()

    def test_snapshot(self):
        b64img = self.poco.snapshot()
        with open('img.jpg', 'wb') as img:
            img.write(base64.b64decode(b64img))

    def test_set_text(self):
        self.poco('com.netease.my:id/netease_mpay__login_urs').set_text('adolli@163.com')

    def test_existence(self):
        self.assertTrue(self.poco('登录').exists())

    def test_existence_after_hide(self):
        btn = self.poco(text='快速游戏', type='android.widget.TextView').focus([0.5, -3])
        btn.click()
        self.assertEqual(btn.exists(), True)
        btn.invalidate()
        self.assertEqual(btn.exists(), False)
        time.sleep(1)
        btn2 = self.poco(text='快速游戏', type='android.widget.Button')
        self.assertEqual(btn2.exists(), True)

    def test_any(self):
        btn = self.poco(text='快速游戏', type='android.widget.TextView').focus([0.5, -3])
        btn.click()
        time.sleep(1)
        print btn.exists()

    def test_dump(self):
        hierarchy = self.poco.agent.hierarchy.dump()
        print hierarchy


class TestRemoteDevice(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.device = Android('a6c29d2b', adbhost=('10.250.190.230', 5038))
        cls.poco = AndroidUiautomationPoco(cls.device)

    def test_any(self):
        for n in self.poco():
            print n.get_name()

