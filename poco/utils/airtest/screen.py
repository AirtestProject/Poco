# coding=utf-8

import base64
import os
from airtest.cli.runner import device as current_device
try:
    from airtest.core.api import snapshot
except ImportError:
    # 兼容旧版本
    from airtest.core.main import snapshot
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
