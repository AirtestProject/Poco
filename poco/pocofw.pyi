# coding=utf-8

from typing import List, Union, NoReturn, Callable, Any, Text

from .acceleration import PocoAccelerationMixin
from .proxy import UIObjectProxy
from .agent import PocoAgent
from .gesture import PendingGestureAction
from .utils.track import MotionTrack


class Poco(PocoAccelerationMixin):
    def __init__(self, agent: PocoAgent, **options) -> Poco:
        self._agent = ...                           # type: PocoAgent
        self._pre_action_wait_for_appearance = 6
        self._post_action_interval = 0.8
        self._poll_interval = 1.44
        self._reevaluate_volatile_attributes = False # type: bool
        self._pre_action_callbacks = []             # type: List[Callable[Text, UIObjectProxy, Any]]
        self._post_action_callbacks = []            # type: List[Callable[Text, UIObjectProxy, Any]]

    def __call__(self, name: Text=None, **kw) -> UIObjectProxy:
        ...

    def wait_for_any(self, objects: List[UIObjectProxy], timeout: float=120.0) -> Union[NoReturn, UIObjectProxy]:
        ...

    def wait_for_all(self, objects: List[UIObjectProxy], timeout: float=120.0) -> NoReturn:
        ...

    def freeze(self) -> Poco:
        ...

    @property
    def agent(self) -> PocoAgent:
        ...

    def click(self, pos: (float, float)):
        ...

    def swipe(self, p1: (float, float), p2: (float, float)=None, direction: (float, float)=None, duration: float=2.0):
        ...

    def long_click(self, pos: (float, float), duration: float=2.0):
        ...

    def scroll(self, direction: Union[List[float], str], percent: float=0.6, duration: float=2.0):
        ...

    def pinch(self, direction: str='in', percent: float=0.6, duration: float=2.0, dead_zone: float=0.1):
        ...

    def pan(self, direction: (float, float), duration: float=2.0):
        ...

    def start_gesture(self, pos: (float, float)) -> PendingGestureAction:
        ...

    def apply_motion_tracks(self, tracks: List[MotionTrack], accuracy: float=0.004):
        ...

    def snapshot(self, width: int=720) -> (str, str):
        ...

    def get_screen_size(self) -> (float, float):
        ...

    def wait_stable(self):
        ...

    def sleep_for_polling_interval(self):
        ...

    def on_pre_action(self, action: Text, ui: UIObjectProxy, args: Any) -> NoReturn:
        ...
    def on_post_action(self, action: Text, ui: UIObjectProxy, args: Any) -> NoReturn:
        ...
    def pre_action(self, action: Text, ui: UIObjectProxy, args: Any) -> NoReturn:
        ...
    def post_action(self, ction: Text, ui: UIObjectProxy, args: Any) -> NoReturn:
        ...
