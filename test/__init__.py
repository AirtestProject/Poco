# coding=utf-8


import time

from tokenid import tokenid, tokenid_g18, tokenid_for_mh
from hunter_cli import Hunter
from poco import Poco


if __name__ == '__main__':
    hunter = Hunter(tokenid, 'g62', devip='10.254.36.254')
    poco = Poco(hunter)
    print poco
