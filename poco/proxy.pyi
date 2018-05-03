# coding=utf-8

from typing import Iterable, Iterator, Text, Tuple, Union, List, Dict, Any

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

    def __getitem__(self, item: int) -> UIObjectProxy:
        ...

    def __iter__(self) -> Iterator[UIObjectProxy]:
        ...

    def swipe(self, direction: (float, float), focus: (float, float)=None, duration=0.5) -> bool:
        ...

    def drag_to(self, target: UIObjectProxy, duration: float=2.0):
        ...

    def start_gesture(self) -> PendingGestureAction:
        ...

    def focus(self, f: (float, float)) -> UIObjectProxy:
        ...

    def get_position(self, focus: (float, float)=None) -> (float, float):
        ...

    def wait(self, timeout: float=3.0) -> UIObjectProxy:
        ...

    def attr(self, name: Text) -> Any:
        ...

    def setattr(self, name: Text, val: Any) -> bool:
        ...

    def exists(self) -> bool:
        ...

    def get_size(self) -> (float, float):
        ...

    def _do_query(self, multiple: bool=True, refresh: bool=False) -> Union[type(None), List[AbstractNode]]:
        ...

    def _direction_vector_of(self, dir_: (float, float)) -> (float, float):
        ...
