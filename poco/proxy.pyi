# coding=utf-8

from typing import Iterable, Iterator, Text, Tuple, Union, List, Dict, Any, NoReturn

from poco.pocofw import Poco
from poco.gesture import PendingGestureAction
from poco.sdk.AbstractNode import AbstractNode

class UIObjectProxy(object):

    def __init__(self, poco, name=None, **attrs) -> UIObjectProxy:
        self.query = ...                    # type: (str, Tuple)
        self.poco = ...                     # type: Poco
        self._query_multiple = ...          # type: bool
        self._evaluated = ...               # type: bool
        self._nodes = ...                   # type: Union[type(None), List[AbstractNode]]
        self._nodes_proxy_is_list = ...     # type: bool
        self._sorted_children = ...         # type: Union[type(None), (UIObjectProxy, (float, float))]
        self._focus = ...                   # type: Union[type(None), (float, float)]

    def child(self, name: Text=None, **attrs) -> UIObjectProxy:
        ...

    def children(self) -> UIObjectProxy:
        ...

    def offspring(self, name: Text=None, **attrs) -> UIObjectProxy:
        ...

    def sibling(self, name: Text=None, **attrs) -> UIObjectProxy:
        ...

    def parent(self) -> UIObjectProxy:
        ...

    def __getitem__(self, item: int) -> UIObjectProxy:
        ...

    def __iter__(self) -> Iterator[UIObjectProxy]:
        ...

    def click(self, focus: (float, float)=None, sleep_interval: float=None) -> bool:
        ...

    def long_click(self, duration: float=2.0) -> bool:
        ...

    def swipe(self, direction: (float, float), focus: (float, float)=None, duration=0.5) -> bool:
        ...

    def drag_to(self, target: UIObjectProxy, duration: float=2.0) -> bool:
        ...

    def scroll(self, direction: Text='vertical', percent: float=0.6, duration: float=2.0) -> bool:
        ...

    def pinch(self, direction: Text='in', percent: float=0.6, duration: float=2.0, dead_zone: float=0.1) -> bool:
        ...

    def start_gesture(self) -> PendingGestureAction:
        ...

    def focus(self, f: (float, float)) -> UIObjectProxy:
        ...

    def get_position(self, focus: (float, float)=None) -> (float, float):
        ...

    def get_text(self) -> Text:
        ...

    def set_text(self, text: Text) -> bool:
        ...

    def get_name(self) -> Text: ...
    def get_size(self) -> (float, float): ...
    def get_bounds(self) -> (float, float, float, float): ...

    @property
    def nodes(self) -> List[AbstractNode]: ...

    def wait(self, timeout: float=3.0) -> UIObjectProxy:
        ...

    def wait_for_appearance(self, timeout: float=120) -> NoReturn: ...
    def wait_for_disappearance(self, timeout: float=120) -> NoReturn: ...

    def attr(self, name: Text) -> Any:
        ...

    def setattr(self, name: Text, val: Any) -> bool:
        ...

    def exists(self) -> bool:
        ...

    def invalidate(self) -> NoReturn:
        ...

    def _do_query(self, multiple: bool=True, refresh: bool=False) -> Union[type(None), List[AbstractNode]]:
        ...

    def _direction_vector_of(self, dir_: (float, float)) -> (float, float):
        ...
