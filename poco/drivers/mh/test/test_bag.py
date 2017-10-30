# coding=utf-8

import unittest

from hunter_cli import Hunter, open_platform
from poco.drivers.mh import MhPoco


class TestBag(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        ipaddr = "10.254.46.45"
        tokenid = open_platform.get_api_token('poco on android')
        cls.poco = MhPoco(addr=(ipaddr, 5001))
        cls.hunter = Hunter(tokenid, 'mh', devip=ipaddr)

    def open_bag(self):
        max_times = 3
        count = 0
        while not self.poco('main/道具').exists():
            self.poco('main/切换按钮动画r').focus('center').click()
            count += 1
            if count >= max_times:
                raise Exception("bag not found")

        self.poco('main/道具').sibling('main/按钮底托').focus('center').click()
        self.poco(type='Button', textMatches='^道.*具$').focus('center').click()

    def server_call(self, cmd):
        self.hunter.script(cmd, lang='text')

    def setUp(self):
        self.server_call('$pckt di')
        self.server_call('$at set ilearncash 0')
        self.server_call('$at set icash 20000000')
        self.server_call('$at set $id iPcktPage 0')
        self.server_call('$at call_txe state_change($id,PROP_PCKTPAGE)')
        self.server_call('$at unlock_all')

        self.open_bag()

    def runTest(self):
        self.poco(type='Button', textMatches='^行.*囊$').focus('center').click()

        # 扩展行囊
        self.poco(text='+').focus('center').click()
        self.poco(text='确定').focus('center').click()
        self.poco(text='确定').focus('center').click()

        moneyCols = self.poco('heroitem_msg.VPanelEquip.HeroItem_Panel_EquipM_UI').child(type='VEdit')
        self.assertTrue(
            all([n.get_text() == '0' for n in moneyCols]),
            "行囊扩展成功"
        )

    def tearDown(self):
        self.poco('vstyle/button/按钮-关闭').focus([0.5, 0]).click()


if __name__ == '__main__':
    unittest.main()
