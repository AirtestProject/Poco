# -*- coding: utf-8 -*-
# @Author: gzliuxin
# @Email:  gzliuxin@corp.netease.com
# @Date:   2017-07-14 19:48:10
from . import MhPoco


def set_forground(title):
    from airtest.core.win import Windows
    dev = Windows()
    handles = dev.find_window_list(title)
    if not handles:
        raise RuntimeError("window not found")
    dev.set_handle(handles[0])
    dev.set_foreground()


if __name__ == '__main__':
    import random
    import time

    p = MhPoco()
    p(textMatches="^比武场\[.+\]$").click("center")
    # p(text="手机也能玩").click()
    # p("超级神虎").click()
    # p("超级神虎").anchor((0, 0)).click()
    # p(text="超级神虎").sibling(type="Button").click()
    l = p(type="CBuffPanel").offspring(type="CDisableImage")
    for i in l:
        i.click()
    # d = p(type="VDialog")
    # while True:
    #     l = d.offspring(type="Button")
    #     r = random.randint(0, len(l.nodes))
    #     try:
    #         i = l[r]
    #     except:
    #         continue
    #     i.click()
