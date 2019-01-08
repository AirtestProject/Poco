# coding=utf-8

from functools import wraps

from airtest.core.api import device as current_device
from airtest.core.api import touch, swipe
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

    def add_preaction_cb(self, driver):
        self._driver = driver
        self._driver.add_pre_action_callback(record_ui)

    def _get_touch_resolution(self):
        """
        get real time resolution on device if full screen
         or window size if running in window mode
        """
        return current_device().get_current_resolution()

    def setTouchDownDuration(self, duration):
        self.default_touch_down_duration = duration

    def getTouchDownDuration(self):
        return self.default_touch_down_duration

    def click(self, x, y):
        pw, ph = self._get_touch_resolution()
        pos = [x * pw, y * ph]
        touch(pos, duration=self.default_touch_down_duration)

    def swipe(self, x1, y1, x2, y2, duration=2.0):
        if duration <= 0:
            raise ValueError("Operation duration cannot be less equal 0. Please provide a positive number.")
        direction = x2 - x1, y2 - y1
        pw, ph = self._get_touch_resolution()
        p1 = [x1 * pw, y1 * ph]
        steps = int(duration * 40) + 1
        swipe(p1, vector=direction, duration=duration, steps=steps)

    def longClick(self, x, y, duration=2.0):
        if duration <= 0:
            raise ValueError("Operation duration cannot be less equal 0. Please provide a positive number.")
        pw, ph = self._get_touch_resolution()
        pos = [x * pw, y * ph]
        touch(pos, duration=duration)

    def applyMotionEvents(self, events):
        if device_platform() != 'Android':
            raise NotImplementedError

        # Android minitouch only, currently
        from airtest.core.android.minitouch import DownEvent, MoveEvent, UpEvent, SleepEvent

        w, h = self._get_touch_resolution()
        mes = []
        for e in events:
            t = e[0]
            if t == 'd':
                contact = e[2]
                x, y = e[1]
                me = DownEvent([x * w, y * h], contact)
            elif t == 'm':
                contact = e[2]
                x, y = e[1]
                me = MoveEvent([x * w, y * h], contact)
            elif t == 'u':
                contact = e[1]
                me = UpEvent(contact)
            elif t == 's':
                how_long = e[1]
                me = SleepEvent(how_long)
            else:
                raise ValueError('Unknown event type {}'.format(repr(t)))
            mes.append(me)

        current_device().minitouch.perform(mes, interval=0)
