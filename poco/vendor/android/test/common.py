# coding=utf-8


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
