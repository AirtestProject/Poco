# -*- coding: utf-8 -*-
# @Author: gzliuxin
# @Email:  gzliuxin@corp.netease.com
# @Date:   2017-07-14 19:48:10
from poco.vendor.mh import MhPoco


def set_forground(title):
    from airtest.core.win import Windows
    dev = Windows()
    handles = dev.find_window_list(title)
    if not handles:
        raise RuntimeError("window not found")
    dev.set_handle(handles[0])
    dev.set_foreground()


if __name__ == '__main__':
    # p = MhPoco(addr=("10.254.45.54", 5001))  # android: Meizu
    p = MhPoco(addr=("10.254.245.124", 5001))  # android: Meizu
    # p = MhPoco(addr=("10.254.42.28", 5001))  # ios: ff's iPad
    # p = MhPoco(addr=("10.211.55.1", 5001))  # windows: parallel
    # p = MhPoco()
    # p(text="长安城").click()
    # p(textMatches="^比武场\[.+\]$").click("center")
    # p(text="手机也能玩").click()
    # p(u"超级神羊").click()
    # p(u"超级神羊").focus((0, 0)).click()
    # p(text="超级神虎").sibling(type="Button").click()
    # l = p(type="CBuffPanel").offspring(type="CDisableImage")
    # for i in l:
    #     i.click()
    l = p(type="CPanel").child(type="AttendanceItem").wait(10)
    print(l.exists())

    # 点日历里的每一项
    # l = p(type="CPanel").child(type="AttendanceItem")
    # for i in l:
    #     i.click("center")

    # while True:
    #     p('loginext/进入互通幻境').click()
    #     p('loginext/确定按钮').focus([0.5, -0.5]).click()
    #     p('loginext/确定按钮').click()


    # for n in p():
    #     print n.get_text()

    # import random
    # import time

    # d = p(type="VDialog")
    # while True:
    #     l = p(type="Button")
    #     r = random.randint(0, len(l.nodes))
    #     try:
    #         i = l[r]
    #     except:
    #         continue
    #     i.click()

    # # 测试截图接口
    # p._rpc_client.getPortSize()
    # from base64 import b64decode
    # d = p._rpc_client.get_screen()
    # with open("screen.png", "wb") as f:
    #     f.write(b64decode(d))
