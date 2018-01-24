# coding=utf-8

import base64
import os
from airtest.cli.runner import device as current_device
try:
    from airtest.core.api import snapshot
except ImportError:
    # 兼容旧版本
    from airtest.core.main import snapshot
from airtest.core.settings import Settings
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
        filename = 'poco-screenshot.png'
        screen_dir = os.path.join(Settings.LOG_DIR, Settings.SCREEN_DIR)
        if not os.path.exists(screen_dir):
            os.makedirs(screen_dir)
        filepath = os.path.join(screen_dir, filename)
        snapshot(filename)
        return base64.b64encode(open(filepath, 'rb').read()), 'png'
