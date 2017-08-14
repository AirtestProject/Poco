# coding=utf-8
__author__ = 'lxn3032'


class ScreenInterface(object):
    def getScreen(self, width):
        """
        获取渲染屏幕的截图
        promisable

        :param width:  预期截图的宽度，渲染屏幕尺度，单位像素
        :return: [图片的base64值 type str，图片格式 'png' 或 'jpg' ... type str]
        """

        raise NotImplementedError

    def getPortSize(self):
        """
        获取渲染屏幕的实际尺寸

        :return: [width, height] type float
        """

        raise NotImplementedError
