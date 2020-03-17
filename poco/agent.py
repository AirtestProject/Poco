# coding=utf-8

from poco.utils.airtest import AirtestInput
from poco.sdk.interfaces.hierarchy import HierarchyInterface
from poco.sdk.interfaces.input import InputInterface
from poco.sdk.interfaces.screen import ScreenInterface
from poco.sdk.interfaces.command import CommandInterface

__author__ = 'lxn3032'


def _assign(val, default_val):
    if isinstance(val, type(None)):
        return default_val
    else:
        return val


class PocoAgent(object):
    """
    This is the agent class for poco to communicate with target device.

    This class is an aggregation of 4 major interfaces for now.

    - :py:class:`HierarchyInterface <poco.sdk.interfaces.hierarchy.HierarchyInterface>`: defines the hierarchy
      accessibility methods such as dump(crawl the whole UI tree), getAttr(retrieve attribute value by name)
    - :py:class:`InputInterface <poco.sdk.interfaces.input.InputInterface>`: defines the simulated input methods to
      allow inject simulated input on target device
    - :py:class:`ScreenInterface <poco.sdk.interfaces.screen.ScreenInterface>`: defines methods to access the screen
      surface
    - :py:class:`CommandInterface <poco.sdk.interfaces.command.CommandInterface>`: defines methods to communicate
      with target device in arbitrary way. This is optional.
    """

    def __init__(self, hierarchy, input, screen, command=None):
        self.hierarchy = _assign(hierarchy, HierarchyInterface())
        self.input = _assign(input, InputInterface())
        self.screen = _assign(screen, ScreenInterface())
        self.command = _assign(command, CommandInterface())
        self._driver = None

    def get_sdk_version(self):
        """
        Retrieve the sdk version from remote runtime. Each poco agent implementation should override this method.

        Returns:
            :py:obj:`str`: version string of the poco sdk. usually in "0.0.0" format. None if not provided by poco sdk.
        """
        pass

    def rpc_reconnect(self):
        self.rpc.close()
        self.rpc.connect()

    @property
    def rpc(self):
        """
        Return the interface of this agent handled.

        Returns:
            :py:obj:`object`: the rpc interface of this agent handled.

        Raises:
            NotImplementedError: raises if the agent implementation dose not expose the rpc interface to user.
        """

        raise NotImplementedError('This poco agent does not have a explicit rpc connection.')

    def on_bind_driver(self, driver):
        self._driver = driver
        if isinstance(self.input, AirtestInput):
            self.input.add_preaction_cb(driver)

    @property
    def driver(self):
        """
        Return the driver of this agent related to. None if the driver is not ready to bind.

        Returns:
            :py:class:`inherit from Poco <poco.pocofw.Poco>`: the driver of this agent related to.
        """

        if not self._driver:
            raise AttributeError("`driver` is not bound on this agent implementation({}). "
                                 "Do you forget to call `super().on_bind_driver` when you override the method "
                                 "`on_bind_driver` in your sub class?"
                                 .format(repr(self)))
        return self._driver
