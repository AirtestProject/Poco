# coding=utf-8


import time

from tokenid import tokenid, tokenid_g18, tokenid_for_mh
from hunter_cli import Hunter
from poco import Poco
from poco.vendor.airtest import AirtestPoco


if __name__ == '__main__':
    hunter = Hunter(tokenid, 'g18', devid='g18_at_10-254-36-219', apihost='192.168.40.111:32022')
    # poco = Poco(hunter)
    ap = AirtestPoco('g18', hunter)
    from airtest.core.main import set_serialno
    set_serialno()
    ap('HeroIcon').click()
    ap('Close').click()
    # print(poco)
    # cb = poco('ConfirmBtn').nodes[0]
    # print(cb.isVisible())
