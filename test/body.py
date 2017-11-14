# coding=utf-8


import json
from hunter_cli import Hunter, open_platform
from poco.drivers.netease.internal import NeteasePoco

if __name__ == '__main__':
    tokenid = open_platform.get_api_token('poco-test')
    # hunter = Hunter(tokenid, 'g62', devid='g62_at_408d5c117d0f')
    hunter = Hunter(tokenid, 'g62', devid='g62_at_408d5c117d0f')
    poco = NeteasePoco('g62', hunter)

    # root = poco.agent.hierarchy.dumper.getRoot()
    # h = poco.agent.hierarchy.dumper.dumpHierarchyImpl(root, False)
    # print json.dumps(h)

    print poco(visible=False).query