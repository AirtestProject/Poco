# coding=utf-8

import unittest


class PocoTestCase(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        """
        相当于airtest的pre脚本
        :return: 
        """

        pass

    def setUp(self):
        """
        初始化一个testcase
        不要把测试逻辑放到这里写，setUp报错的话也相当于真个case报错

        """

        pass

    def runTest(self):
        """
        testcase的正文，把要执行的测试和包括断言语句都写到这里

        """

        raise NotImplementedError

    def tearDown(self):
        """
        一个testcase的清场工作

        """

        pass

    @classmethod
    def tearDownClass(cls):
        """
        airtest的post脚本
        :return: 
        """

        pass

    def shortDescription(self):
        """
        描述这个testcase的细节，如果需要的话就override这个方法
        
        :return: <str>
        """

        return super(PocoTestCase, self).shortDescription()

