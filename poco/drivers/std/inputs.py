# coding=utf-8

from poco.sdk.interfaces.input import InputInterface


class StdInput(InputInterface):
    def __init__(self, client):
        super(StdInput, self).__init__()
        self.client = client
        # 根据需要修改构造函数的签名
        # 并修改对应的调用处

    def click(self, x, y):
        pass

    def swipe(self, x1, y1, x2, y2, duration):
        pass

    def longClick(self, x, y, duration):
        pass

    def keyevent(self, keycode):
        pass
