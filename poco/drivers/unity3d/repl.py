# coding=utf-8

import json
import sys
import traceback

from poco.drivers.unity3d import UnityPoco
from airtest.core.api import connect_device


def process_cmd(cmd):
    try:
        print('cmd', cmd)
        exec(cmd)
    except:
        traceback.print_exc()


if __name__ == '__main__':
    print('hello poco unity3d repl!')

    while True:
        cmd = sys.stdin.readline()
        try:
            # print('cmd', cmd)
            exec(cmd)
        except Exception as e:
            traceback.print_exc()
