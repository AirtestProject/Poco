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
    p(name=u"超级神虎").click(anchor=(0.5, 0.5))
    p(text=u"超级神虎").sibling(type="Button").click()
    # p(text=u"手机也能玩").click()
    # l = p(type="CBuffPanel").offspring(type="CDisableImage")
    # while True:
    #     l = p(typeMatches="^.*$")
    #     r = random.randint(0, len(l.nodes))
    #     print(len(l.nodes), r)
    #     try:
    #         i = l[r]
    #     except:
    #         continue
    #     r2 = random.randint(0, 100)
    #     if r2 < 15:
    #         op = "right"
    #     else:
    #         op = "left"
    #     i.click(op=op)
