# coding=utf-8
__author__ = 'lxn3032'


class ScreenInterface(object):
    """
    This is one of the main communication interfaces. This interface ensures the ability for accessing the rendering
    the results presented on screen of target device. Note that rendering results are very often not used in automated
    testing directly. Following methods definitions can assist to obtain the information about the app.
    """

    def getScreen(self, width):
        """
        Take the screenshot of the target device screen or target app's window

        Args:
            width (:obj:`int`): expected width of the screenshot in pixels

        Returns:
            2-:obj:`list` (:obj:`str`, :obj:`str`):
                - b64img: base64 encoded screen data
                - format: screen data format (png/jpg/etc.)
        """

        raise NotImplementedError

    def getPortSize(self):
        """
        Get the real resolution of the screen in pixels.

        Returns:
            2-:obj:`list` (:obj:`float`, :obj:`float`): width and height in pixels
        """

        raise NotImplementedError
