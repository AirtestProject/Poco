# coding=utf-8


import unittest

from poco.unittest.case import PocoTestCase


class TestPocoRunner(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        pass

    def test_run(_):
        class MyCase(PocoTestCase):
            def setUp(self):
                print('setup')
                self.value = '2333'

            def runTest(self):
                print('before')
                self.assertEqual(1, 1, 'ok')
                self.assertEqual(self.value, '2333', 'setup ok')
                print('after')

            def tearDown(self):
                print('teardown')

        suite = unittest.TestSuite()
        suite.addTest(MyCase())

        runner = unittest.TextTestRunner()
        runner.run(suite)
