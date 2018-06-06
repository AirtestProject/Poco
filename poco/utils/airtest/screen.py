# coding=utf-8

import base64
from airtest.core.api import snapshot, device as current_device
from poco.sdk.interfaces.screen import ScreenInterface


class AirtestScreen(ScreenInterface):
    def __init__(self):
        super(AirtestScreen, self).__init__()

    def getPortSize(self):
        disp = current_device().display_info
        if disp['orientation'] in (1, 3):
            return [disp['height'], disp['width']]
        else:
            return [disp['width'], disp['height']]

    def getScreen(self, width):
        savepath = snapshot()
        return base64.b64encode(open(savepath, 'rb').read()), 'png'
