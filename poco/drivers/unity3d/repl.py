# coding=utf-8

import re
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

    buf = ''
    while True:
        line = sys.stdin.readline().rstrip() + '\n'
        buf += line
        if re.findall(r'# end-proc #\s*$', buf):
            try:
                # print('cmd', buf)
                cmd = buf
                buf = ''
                exec(cmd)
            except Exception as e:
                traceback.print_exc()
