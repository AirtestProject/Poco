# coding=utf-8
__author__ = 'lxn3032'


class ScreenInterface(object):
    def snapshot(self, width):
        """
        获取渲染屏幕的截图

        :param width:  预期截图的宽度，渲染屏幕尺度，单位像素
        :return: [图片的base64值 type str，图片格式 'png' 或 'jpg' ... type str]
        """

        raise NotImplementedError

    def get_screen_size(self):
        """
        获取渲染屏幕的实际尺寸，type float

        :return:  [width, height] as floats 
        """

        raise NotImplementedError
