# coding=utf-8

import base64
import os

from airtest.cli.runner import device as current_device
from airtest.core.main import snapshot
from airtest.core.settings import Settings
from poco.sdk.interfaces.screen import ScreenInterface


class AirtestScreen(ScreenInterface):
    def __init__(self):
        super(AirtestScreen, self).__init__()

    def getPortSize(self):
        disp = current_device().get_display_info()
        return [disp['width'], disp['height']]

    def getScreen(self, width):
        filename = 'poco-screenshot.png'
        filepath = os.path.join(Settings.LOG_DIR, Settings.SCREEN_DIR, filename)
        snapshot(filepath)
        return base64.b64encode(open(filepath, 'rb').read()), 'png'
