# coding=utf-8

from airtest.cli.runner import device as current_device
from airtest.core.main import snapshot
from poco.sdk.interfaces.screen import ScreenInterface


class AirtestScreen(ScreenInterface):
    def __init__(self):
        super(AirtestScreen, self).__init__()

    def getPortSize(self):
        disp = current_device().get_display_info()
        return [disp['width'], disp['height']]

    def getScreen(self, width):
        # TODO: 这里要把截图内容返回
        snapshot()
