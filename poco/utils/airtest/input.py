# coding=utf-8

from functools import wraps

from airtest.core.api import device as current_device
from airtest.core.api import touch, swipe, double_click
from airtest.core.helper import device_platform, logwrap
from poco.sdk.interfaces.input import InputInterface

__all__ = ['AirtestInput']


def serializable_adapter(func):
    class ISerializable(object):
        def to_json(self):
            raise NotImplementedError

    @wraps(func)
    def wrapped(*args):
        class PocoUIProxySerializable(ISerializable):
            def __init__(self, obj):
                self.obj = obj

            def to_json(self):
                return repr(self.obj)

        new_args = [PocoUIProxySerializable(a) for a in args]
        return func(*new_args)

    return wrapped


@serializable_adapter
@logwrap
def record_ui(driver, action, ui, args):
    return ui


class AirtestInput(InputInterface):
    def __init__(self):
        super(AirtestInput, self).__init__()
        self.default_touch_down_duration = 0.01
        self._driver = None
        self.use_render_resolution = False
        self.render_resolution = None

    def add_preaction_cb(self, driver):
        self._driver = driver
        self._driver.add_pre_action_callback(record_ui)

    def get_target_pos(self, x, y):
        """
        get real time resolution on device of target (x,y)
        """
        offsetx, offsety, pw, ph = self._get_touch_resolution()
        pos = [x * pw + offsetx, y * ph + offsety]
        return pos

    def _get_touch_resolution(self):
        """
        get real time resolution on device if full screen
         or window size if running in window mode
        """
        if device_platform() == 'Android':
            if self.use_render_resolution:
                if self.render_resolution and len(self.render_resolution) == 4:
                    return self.render_resolution
                else:
                    return current_device().get_render_resolution()
        w, h = current_device().get_current_resolution()
        return 0, 0, w, h

    def setTouchDownDuration(self, duration):
        self.default_touch_down_duration = duration

    def getTouchDownDuration(self):
        return self.default_touch_down_duration

    def click(self, x, y):
        pos = self.get_target_pos(x, y)
        touch(pos, duration=self.default_touch_down_duration)

    def double_click(self, x, y):
        pos = self.get_target_pos(x, y)
        double_click(pos)

    def swipe(self, x1, y1, x2, y2, duration=2.0):
        if duration <= 0:
            raise ValueError("Operation duration cannot be less equal 0. Please provide a positive number.")
        direction = x2 - x1, y2 - y1
        pos = self.get_target_pos(x1, y1)
        steps = int(duration * 40) + 1
        swipe(pos, vector=direction, duration=duration, steps=steps)

    def longClick(self, x, y, duration=2.0):
        if duration <= 0:
            raise ValueError("Operation duration cannot be less equal 0. Please provide a positive number.")
        pos = self.get_target_pos(x, y)
        touch(pos, duration=duration)

    def applyMotionEvents(self, events):
        if device_platform() != 'Android':
            raise NotImplementedError

        # Android minitouch/maxtouch only, currently
        from airtest.core.android.touch_methods.base_touch import DownEvent, MoveEvent, UpEvent, SleepEvent

        mes = []
        for e in events:
            t = e[0]
            if t == 'd':
                contact = e[2]
                x, y = e[1]
                pos = self.get_target_pos(x, y)
                me = DownEvent(pos, contact)
            elif t == 'm':
                contact = e[2]
                x, y = e[1]
                pos = self.get_target_pos(x, y)
                me = MoveEvent(pos, contact)
            elif t == 'u':
                contact = e[1]
                me = UpEvent(contact)
            elif t == 's':
                how_long = e[1]
                me = SleepEvent(how_long)
            else:
                raise ValueError('Unknown event type {}'.format(repr(t)))
            mes.append(me)

        current_device().touch_proxy.perform(mes, interval=0)
