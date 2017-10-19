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

        Args:
            width (:obj:`int`): Expected screen shot width in pixels.

        Returns:
            :obj:`str`: Base64 encoded screen data.
        """

        raise NotImplementedError

    def getPortSize(self):
        """
        Get the real resolution in pixels of the screen.

        Returns:
            2-:obj:`list` (:obj:`float`, :obj:`float`): 
                - width
                - height
        """

        raise NotImplementedError
