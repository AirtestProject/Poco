# coding=utf-8

import time
import unittest

from poco.drivers.cocosjs import CocosJsPoco


class SimpleTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.poco = CocosJsPoco("ws://localhost:15003")

    @classmethod
    def tearDownClass(cls):
        time.sleep(1)

    def test_dump(self):
        print(self.poco.agent.hierarchy.dump())
