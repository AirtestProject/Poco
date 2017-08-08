# coding=utf-8


import unittest

from hunter_cli import open_platform, Hunter
from poco.vendor.local.Dumper import Dumper
from poco.vendor.local import LocalPoco
from poco.vendor.airtest import AirtestPoco


class TestCommon(unittest.TestCase):
    def test_make_tree(self):
        tokenid = open_platform.get_api_token('g18')
        hunter = AirtestHunter(tokenid, 'g18')
        poco = AirtestPoco('g18', hunter)
        dumper = Dumper(poco.rpc.dump())
        print dumper.dumpHierarchy()

    def test_local_init(self):
        tokenid = open_platform.get_api_token('local-poco', 'g18')
        hunter = Hunter(tokenid, 'g18', devid='g18_at_10-254-245-31', apihost='10.251.90.33:32022')
        dumpalbe = hunter.refer('support.poco.cocos2dx.Dumper')

        poco = LocalPoco(dumpalbe)
        for n in poco():
            print n.get_name()
