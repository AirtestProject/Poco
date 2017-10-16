# coding=utf-8
__author__ = 'lxn3032'


class ScreenInterface(object):
    """
    This is one of the main communication interfaces. This interface ensure the ability of accessing the rendering 
    results presented on screen of target device. Rendering results are sometimes not used in automated testing 
    directly. The method defines as following can assist in obtaining information about the app.
    """

    def getScreen(self, width):
        """
        Take a screen shot of target device or target app's window.
        获取渲染屏幕的截图。

        :param width: Expected screen shot width in pixels.
        :return: Base64 encoded screen data in <type str>. 
        """

        raise NotImplementedError

    def getPortSize(self):
        """
        Get the real resolution in pixles of the screen.
        获取渲染屏幕的实际尺寸。

        :return: [width, height] in pixels in <type float>.
        """

        raise NotImplementedError
