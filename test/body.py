# coding=utf-8


import time

# from tokenid import tokenid, tokenid_g18, tokenid_for_mh
from hunter_cli import Hunter, open_platform
from poco import Poco
from poco.vendor.airtest import AirtestPoco
from hrpc.client import RpcClient


if __name__ == '__main__':
    tokenid = open_platform.get_api_token('poco-test', 'g18')
    hunter = Hunter(tokenid, 'g18', devid='g18_at_10-254-245-31', apihost='10.251.90.33:32022')
    # poco = Poco(hunter)
    poco = AirtestPoco('g18', hunter)
    # from airtest.core.main import set_serialno
    # set_serialno()
    # ap('HeroIcon').click()
    # ap('Close').click()
    panels = poco('MainPanel').offspring('Panel').child('Panel')
    print len(panels.nodes)
    # n = panels.nodes[1]
    # # n = poco.agent._rpc_client.evaluate(n)
    # print n
    # # n = panels[1].nodes
    # print '+++', '_evaluated__:', n._evaluated__, 'uri:', n._uri__, 'is_intermediate:', n._is_intermediate_uri__
