# coding=utf-8

import base64
import time
import unittest

from poco.drivers.std import StdPoco
from airtest.core.api import connect_device, device as current_device


class TestSimple(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        connect_device('Android:///')
        cls.poco = StdPoco()

    @classmethod
    def tearDownClass(cls):
        time.sleep(2)

    def test_dump(self):
        print self.poco.agent.hierarchy.dump()

    def test_getSdkVersion(self):
        print self.poco.agent.get_sdk_version()

    def test_nosuch_rpc_method(self):
        print self.poco.agent.get_debug_profiling_data()

    def test_get_screen(self):
        b64img, fmt = self.poco.snapshot()
        with open('screen.{}'.format(fmt), 'wb') as f:
            f.write(base64.b64decode(b64img))

    def test_get_screen_size(self):
        print self.poco.get_screen_size()
