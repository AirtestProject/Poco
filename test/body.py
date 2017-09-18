# coding=utf-8


import time

# from tokenid import tokenid, tokenid_g18, tokenid_for_mh
from hunter_cli import Hunter, open_platform
from poco import Poco
from poco.vendor.airtest import AirtestPoco
from hrpc.client import RpcClient
from poco.vendor.cocosjs import CocosJsPoco


if __name__ == '__main__':
    tokenid = open_platform.get_api_token('poco-test')
    # hunter = Hunter(tokenid, 'g62', devid='g62_at_408d5c117d0f')
    hunter = Hunter(tokenid, 'g37', devid='g37_at_863542037875892')
    poco = AirtestPoco('g37', hunter)

    # print poco(textMatches='.*入游戏').get_text()
    for n in poco('root').child('Layout').child('Layout').child('Layout').offspring('Label', textMatches='^\d\d:\d\d$').sibling(type='Sprite'):
        print n.get_position()

        # print ui.get_bounds()
    # poco = AirtestPoco('g18', hunter)
    # from airtest.core.main import set_serialno
    # set_serialno()
    # ap('HeroIcon').click()
    # ap('Close').click()
    # panels = poco('MainPanel').offspring('Panel').child('Panel')
    # print len(panels.nodes)
    # n = panels.nodes[1]
    # print n
    # # n = panels[1].nodes
    #
    # poco = CocosJsPoco()
    # for p in poco():
    #     print p
