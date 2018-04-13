# coding=utf-8

from poco.sdk.interfaces.screen import ScreenInterface
from poco.utils.simplerpc.utils import sync_wrapper


class StdScreen(ScreenInterface):
    def __init__(self, client):
        super(StdScreen, self).__init__()
        self.client = client

    @sync_wrapper
    def getScreen(self, width):
        return self.client.call("Screenshot", width)

    @sync_wrapper
    def getPortSize(self):
        return self.client.call("GetScreenSize")
