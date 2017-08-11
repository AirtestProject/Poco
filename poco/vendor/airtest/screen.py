# coding=utf-8

from poco.interfaces import ScreenInterface

from airtest.core.main import snapshot


class AirtestScreen(ScreenInterface):
    def __init__(self, remote_screen_proxy):
        self.screen = remote_screen_proxy

    def get_screen_size(self):
        return [float(s) for s in self.screen.getPortSize()]

    def snapshot(self, width):
        snapshot()

    # def get_input_panel_size(self):
    #     screen_w, screen_h = self.get_screen_size()
    #     display_info = current_device().get_display_info()
    #     real_w, real_h = display_info['width'], display_info['height']
    #     if screen_w > screen_h:
    #         w = max(real_w, real_h)
    #         h = min(real_w, real_h)
    #     else:
    #         w, h = real_w, real_h
    #     return [float(w), float(h)]  # 用于进行输入的分辨率，与设备输入接口对应
