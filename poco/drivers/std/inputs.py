# coding=utf-8

from poco.sdk.interfaces.input import InputInterface
from poco.utils.simplerpc.utils import sync_wrapper


class StdInput(InputInterface):
    def __init__(self, client):
        super(StdInput, self).__init__()
        self.client = client
        # 根据需要修改构造函数的签名
        # 并修改对应的调用处

    @sync_wrapper
    def click(self, x, y):
        return self.client.call("Click", x, y)

    @sync_wrapper
    def swipe(self, x1, y1, x2, y2, duration):
        return self.client.call("Swipe", x1, y1, x2, y2, duration)

    @sync_wrapper
    def longClick(self, x, y, duration):
        return self.client.call("LongClick", x, y, duration)

    @sync_wrapper
    def keyevent(self, keycode):
        return self.client.call("KeyEvent", keycode)

    @sync_wrapper
    def scroll(self, direction='vertical', percent=1, duration=2.0):
        return self.client.call("Scroll", direction, percent, duration)

    @sync_wrapper
    def rclick(self, x, y):
        return self.client.call("RClick", x, y)

    @sync_wrapper
    def double_click(self, x, y):
        return self.client.call("DoubleClick", x, y)
