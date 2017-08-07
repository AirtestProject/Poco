# coding=utf-8


import time
import base64
import unittest

from poco.vendor.android.uiautomation import AndroidUiautomationPoco


class TextCommonCases(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.poco = AndroidUiautomationPoco()

    def test_snapshot(self):
        b64img = self.poco.snapshot()
        with open('img.jpg', 'wb') as img:
            img.write(base64.b64decode(b64img))

    def test_existence(self):
        print self.poco('登录').exists()

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
        self.poco(resourceIdMatches='^.*switch_account$').click()
