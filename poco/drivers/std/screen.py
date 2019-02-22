# coding=utf-8

import base64
import zlib

from poco.sdk.interfaces.screen import ScreenInterface
from poco.utils.simplerpc.utils import sync_wrapper


class StdScreen(ScreenInterface):
    def __init__(self, client):
        super(StdScreen, self).__init__()
        self.client = client

    @sync_wrapper
    def _getScreen(self, width):
        return self.client.call("Screenshot", width)

    def getScreen(self, width):
        b64, fmt = self._getScreen(width)
        if fmt.endswith('.deflate'):
            fmt = fmt[:-len('.deflate')]
            imgdata = base64.b64decode(b64)
            imgdata = zlib.decompress(imgdata)
            b64 = base64.b64encode(imgdata)
        return b64, fmt

    @sync_wrapper
    def getPortSize(self):
        return self.client.call("GetScreenSize")