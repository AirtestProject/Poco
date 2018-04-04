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
        b64img, fmt = self.poco.snapshot()
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
        from airtest.core.api import connect_device
        connect_device('Android:///HT7C51A04625')
        cls.poco = AndroidUiautomationPoco(use_airtest_input=True)

    def test_any(self):
        self.poco('com.netease.cloudmusic:id/mn').click()
        self.poco('com.netease.cloudmusic:id/aib').click()
        jpg, fmt = self.poco.snapshot()
        print(len(jpg), fmt)
        time.sleep(5)


class TestConcurrentAccess(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        from airtest.core.api import connect_device
        connect_device('Android:///HT7C51A04625')
        # cls.p = AndroidUiautomationPoco()
        cls.pocos = [AndroidUiautomationPoco() for _ in range(3)]

    @classmethod
    def tearDownClass(cls):
        for poco in cls.pocos:
            print poco._instrument_proc
        time.sleep(2)

    def test_dump_hierarchy(self):
        for poco in self.pocos:
            h = poco.agent.hierarchy.dump()
            print len(h)

