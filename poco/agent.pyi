# coding=utf-8

from typing import Iterable, Iterator, Text, Tuple, Union, List, Dict, Any, NoReturn

from poco.pocofw import Poco
from poco.sdk.interfaces.hierarchy import HierarchyInterface
from poco.sdk.interfaces.input import InputInterface
from poco.sdk.interfaces.screen import ScreenInterface
from poco.sdk.interfaces.command import CommandInterface


class PocoAgent(object):
    def __init__(self,
                 hierarchy: HierarchyInterface,
                 input: InputInterface,
                 screen: ScreenInterface,
                 command: CommandInterface=None):
        self.hierarchy = ...    # type: HierarchyInterface
        self.input = ...        # type: InputInterface
        self.screen = ...       # type: ScreenInterface
        self.command = ...      # type: CommandInterface
        self._driver = ...      # type: Poco

    def get_sdk_version(self) -> Text:
        ...

    @property
    def rpc(self) -> Any:
        ...

    def on_bind_driver(self, driver: Poco) -> NoReturn:
        ...

    @property
    def driver(self) -> Poco:
        ...
