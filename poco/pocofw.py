# coding=utf-8
from __future__ import unicode_literals

import time
import traceback
import warnings

from .acceleration import PocoAccelerationMixin
from .exceptions import PocoTargetTimeout, InvalidOperationException
from .proxy import UIObjectProxy
from .agent import PocoAgent
from .freezeui.utils import create_immutable_hierarchy
from .utils.track import MotionTrackBatch
from .utils.multitouch_gesture import make_pinching
from .gesture import PendingGestureAction

__author__ = 'lxn3032'


class Poco(PocoAccelerationMixin):
    """
    Poco standard initializer.

    Args:
        agent (:py:class:`PocoAgent <poco.agent.PocoAgent>`): an agent object for Poco to communicate with the target
         device. See :py:class:`PocoAgent <poco.agent.PocoAgent>` definition for more details.
        options:
            - ``action_interval``: time interval to wait for the action (such as touch or swipe) completion performed
              on device and for the UI to become still (stable). Default value is 0.8s.
            - ``poll_interval``: the minimum time needed between each poll events (such as waiting for UI element to
              appear on the screen). Polling is done periodically.
            - ``pre_action_wait_for_appearance``: time interval to wait before the action (such as click or swipe) is
              performed. If the target UI element does not appear on the screen after this time interval, the
              :py:class:`PocoNoSuchNodeException <poco.exceptions.PocoNoSuchNodeException>` is raised
            - ``touch_down_duration``: Touch down step duration of the click operation last for. If this argument is
              provided, this value will set to ``self.agent.input`` module. Note that not all implementation of poco 
              support this parameter. If not support, you may see a warning.
            - ``reevaluate_volatile_attributes``: Re-select target UI proxy when retrieving volatile attributes. Poco
              drivers that using hrpc connections should default to be ``False`` as hrpc always reevaluate the
              attributes remotely. This option is useful for ``StdPoco`` driver and should be handled by ``StdPoco``.
    """

    def __init__(self, agent, **options):
        super(Poco, self).__init__()
        self._agent = agent

        # options
        self._pre_action_wait_for_appearance = options.get('pre_action_wait_for_appearance', 6)
        self._post_action_interval = options.get('action_interval', 0.8)
        self._poll_interval = options.get('poll_interval', 1.44)
        self._reevaluate_volatile_attributes = options.get('reevaluate_volatile_attributes', False)
        if 'touch_down_duration' in options:
            touch_down_duration = options['touch_down_duration']
            try:
                touch_down_duration = float(touch_down_duration)
            except ValueError:
                raise ValueError('Option `touch_down_duration` should be <float>. Got {}'
                                 .format(repr(touch_down_duration)))
            self._agent.input.setTouchDownDuration(touch_down_duration)

        self._pre_action_callbacks = [self.__class__.on_pre_action]
        self._post_action_callbacks = [self.__class__.on_post_action]
        self._agent.on_bind_driver(self)

    def __call__(self, name=None, **kw):
        """
        Call Poco instance to select the UI element by query expression. Query expression can contain specific name
        and/or other attributes. Invisible UI elements will be skipped even if "visible=False" argument is set.

        Selection process is not executed instantly, the query expression is stored in the UI proxy and the selection is
        executed only then when the UI element(s) info is required (such get the point coordinates where to click, 
        and/or retrieve the specific attribute value).

        Examples:
            This example shows selecting a Button named 'close'::

                poco = Poco(...)
                close_btn = poco('close', type='Button')

        Args:
            name (:obj:`str`): name of the UI element to be selected

        Keyword Args:
            xx: arbitrary key value pair that stands for selecting the UI matching the value of ``UI.xx``
            xxMatches (:obj:`str`): arbitrary key value pair that stands for selecting the UI matching the regular 
             expression pattern ``UI.xx``

        In keyword args, you can only use `xx` or `xxMatches` at the same time. Using both with the same attribute does
        not make sense. Besides, `xx` should not start with ``_`` (underscore) as attributes start with ``_`` are 
        private attributes that used by sdk implementation.
        ::

            # select the UI element(s) which text attribute matches the pattern '^close.*$'
            poco = Poco(...)
            arb_close_btn = poco(textMatches='^close.*$')

        Returns:
            :py:class:`UIObjectProxy <poco.proxy.UIObjectProxy>`: UI proxy object representing the UI element matches 
            the given query expression.
        """

        if not name and len(kw) == 0:
            warnings.warn("Wildcard selector may cause performance trouble. Please give at least one condition to "
                          "shrink range of results")
        return UIObjectProxy(self, name, **kw)

    def wait_for_any(self, objects, timeout=120):
        """
        Wait until any of given UI proxies show up before timeout and return the first appeared UI proxy.
        All UI proxies will be polled periodically. See options :py:class:`poll_interval <poco.pocofw.Poco>` in
        ``Poco``'s initialization for more details.

        Args:
            objects (Iterable<:py:class:`UIObjectProxy <poco.proxy.UIObjectProxy>`>): iterable object of the given UI 
             proxies
            timeout (:obj:`float`): timeout in seconds, default is 120s

        Returns:
            :py:class:`UIObjectProxy <poco.proxy.UIObjectProxy>`: the first appeared UI proxy

        Raises:
            PocoTargetTimeout: when none of UI proxies appeared before timeout
        """

        start = time.time()
        while True:
            for obj in objects:
                if obj.exists():
                    return obj
            if time.time() - start > timeout:
                raise PocoTargetTimeout('any to appear', objects)
            self.sleep_for_polling_interval()

    def wait_for_all(self, objects, timeout=120):
        """
        Wait until all of given UI proxies show up before timeout.
        All UI proxies will be polled periodically. See option :py:class:`poll_interval <poco.pocofw.Poco>` in 
        ``Poco``'s initialization for more details.

        Args:
            objects (Iterable<:py:class:`UIObjectProxy <poco.proxy.UIObjectProxy>`>): iterable object of the given UI 
             proxies
            timeout (:obj:`float`): timeout in seconds, default is 120s

        Raises:
            PocoTargetTimeout: when not all of UI proxies appeared before timeout
        """

        start = time.time()
        while True:
            all_exist = True
            for obj in objects:
                if not obj.exists():
                    all_exist = False
                    break
            if all_exist:
                return
            if time.time() - start > timeout:
                raise PocoTargetTimeout('all to appear', objects)
            self.sleep_for_polling_interval()

    def freeze(this):
        """
        Snapshot current **hierarchy** and cache it into a new poco instance. This new poco instance is a copy from
        current poco instance (``self``). The hierarchy of the new poco instance is fixed and immutable. It will be
        super fast when calling ``dump`` function from frozen poco. See the example below.
        
        Examples:
            ::

                poco = Poco(...)
                frozen_poco = poco.freeze()
                hierarchy_dict = frozen_poco.agent.hierarchy.dump()  # will return the already cached hierarchy data
                

        Returns:
            :py:class:`Poco <poco.pocofw.Poco>`: new poco instance copy from current poco instance (``self``)
        """

        class FrozenPoco(Poco):
            def __init__(self, **kwargs):
                hierarchy_dict = this.agent.hierarchy.dump()
                hierarchy = create_immutable_hierarchy(hierarchy_dict)
                agent_ = PocoAgent(hierarchy, this.agent.input, this.agent.screen)
                kwargs['action_interval'] = 0.01
                kwargs['pre_action_wait_for_appearance'] = 0
                super(FrozenPoco, self).__init__(agent_, **kwargs)
                self.this = this

            def __enter__(self):
                return self

            def __exit__(self, exc_type, exc_val, exc_tb):
                pass

            def __getattr__(self, item):
                return getattr(self.this, item)

        return FrozenPoco()

    def wait_stable(self):
        """
        Sleep for fixed number of seconds in order to wait for the UI to become still (stable).
        There is no need to call this method manually. It's automatically invoked when required.
        """

        time.sleep(self._post_action_interval)

    def sleep_for_polling_interval(self):
        """
        Sleep for fixed number of seconds after each poll event.
        There is no need to call this method manually. It's automatically invoked when required.
        """

        time.sleep(self._poll_interval)

    @property
    def agent(self):
        """
        Readonly property to access poco agent instance. See :py:class:`poco.agent.PocoAgent` for more details.

        Returns:
            :py:class:`poco.agent.PocoAgent`: poco agent instance
        """

        return self._agent

    def click(self, pos):
        """
        Perform click (touch, tap, etc.) action on target device at given coordinates.

        The coordinates (x, y) are either a 2-list or 2-tuple. The coordinates values for x and y must be in the
        interval between 0 ~ 1 to represent the percentage of the screen. For example, the coordinates ``[0.5, 0.5]``
        represent the `center` of the screen and the coordinates ``[0, 0]`` represent the `top left corner`.

        See ``CoordinateSystem`` for more details about coordinate system.

        Examples:
            Click the point of ``(100, 100)`` of screen which resolution is ``(1920, 1080)``::

                poco.click([100.0 / 1920, 100.0 / 1080])

        Args:
            pos (:obj:`list(float, float)` / :obj:`tuple(float, float)`): coordinates (x, y) in range of 0 to 1

        Raises:
            InvalidOperationException: when clicked outside of the screen
        """

        if not (0 <= pos[0] <= 1) or not (0 <= pos[1] <= 1):
            raise InvalidOperationException('Click position out of screen. pos={}'.format(repr(pos)))
        ret = self.agent.input.click(pos[0], pos[1])
        self.wait_stable()
        return ret

    def rclick(self, pos):
        raise NotImplementedError

    def double_click(self, pos):
        ret = self.agent.input.double_click(pos[0], pos[1])
        self.wait_stable()
        return ret

    def swipe(self, p1, p2=None, direction=None, duration=2.0):
        """
        Perform swipe action on target device from point to point given by start point and end point, or by the
        direction vector. At least one of the end point or direction must be provided.

        The coordinates (x, y) definition for points is the same as for ``click`` event. The components of the
        direction vector (x, y) are also expressed in the range of the screen from 0 to 1.

        See ``CoordinateSystem`` for more details about coordinate system.

        Examples:
            Following example shows how to perform a swipe action from (100, 100) to (100, 200) on screen with
            resolution 1920x1080::

                poco.swipe([100.0 / 1920, 100.0 / 1080], [100.0 / 1920, 200.0 / 1080])

            Or given by the specific direction instead of end point::

                poco.swipe([100.0 / 1920, 100.0 / 1080], direction=[0, 100.0 / 1080])

        Args:
            p1 (:obj:`2-list/2-tuple`): start point
            p2: end point
            direction: swipe direction
            duration (:obj:`float`): time interval in which the swipe action is performed

        Raises:
            InvalidOperationException: when the start point of the swipe action lies outside the screen
        """

        try:
            duration = float(duration)
        except ValueError:
            raise ValueError('Argument `duration` should be <float>. Got {}'.format(repr(duration)))

        if not (0 <= p1[0] <= 1) or not (0 <= p1[1] <= 1):
            raise InvalidOperationException('Swipe origin out of screen. {}'.format(repr(p1)))
        if direction is not None:
            p2 = [p1[0] + direction[0], p1[1] + direction[1]]
        elif p2 is not None:
            p2 = p2
        else:
            raise TypeError('Swipe end not set.')
        return self.agent.input.swipe(p1[0], p1[1], p2[0], p2[1], duration)

    def long_click(self, pos, duration=2.0):
        """
        Similar to click but press the screen for the given time interval and then release

        Args:
            pos (:obj:`2-list/2-tuple`): coordinates (x, y) in range from 0 to 1
            duration: duration of press the screen
        """

        try:
            duration = float(duration)
        except ValueError:
            raise ValueError('Argument `duration` should be <float>. Got {}'.format(repr(duration)))

        if not (0 <= pos[0] <= 1) or not (0 <= pos[1] <= 1):
            raise InvalidOperationException('Click position out of screen. {}'.format(repr(pos)))
        return self.agent.input.longClick(pos[0], pos[1], duration)

    def scroll(self, direction='vertical', percent=0.6, duration=2.0):
        """
        Scroll from the lower part to the upper part of the entire screen.

        Args:
            direction (:py:obj:`str`): scrolling direction. "vertical" or "horizontal"
            percent (:py:obj:`float`): scrolling distance percentage of the entire screen height or width according to
             direction
            duration (:py:obj:`float`): time interval in which the action is performed
        """

        if direction not in ('vertical', 'horizontal'):
            raise ValueError('Argument `direction` should be one of "vertical" or "horizontal". Got {}'
                             .format(repr(direction)))

        start = [0.5, 0.5]
        half_distance = percent / 2
        if direction == 'vertical':
            start[1] += half_distance
            direction = [0, -percent]
        else:
            start[0] += half_distance
            direction = [-percent, 0]

        return self.swipe(start, direction=direction, duration=duration)

    def pinch(self, direction='in', percent=0.6, duration=2.0, dead_zone=0.1):
        """
        Squeezing or expanding 2 fingers on the entire screen.

        Args:
            direction (:py:obj:`str`): pinching direction, only "in" or "out". "in" for squeezing, "out" for expanding
            percent (:py:obj:`float`): squeezing range from or expanding range to of the entire screen
            duration (:py:obj:`float`): time interval in which the action is performed
            dead_zone (:py:obj:`float`): pinching inner circle radius. should not be greater than ``percent``
        """

        if direction not in ('in', 'out'):
            raise ValueError('Argument `direction` should be one of "in" or "out". Got {}'.format(repr(direction)))
        if dead_zone >= percent:
            raise ValueError('Argument `dead_zone` should not be greater than `percent`. dead_zoon={}, percent={}'
                             .format(repr(dead_zone), repr(percent)))

        tracks = make_pinching(direction, [0.5, 0.5], [1, 1], percent, dead_zone, duration)
        speed = (percent - dead_zone) / 2 / duration

        # 速度慢的时候，精度适当要提高，这样有助于控制准确
        ret = self.apply_motion_tracks(tracks, accuracy=speed * 0.03)
        return ret

    def pan(self, direction, duration=2.0):
        raise NotImplementedError

    def start_gesture(self, pos):
        """
        Start a gesture action. This method will return a :py:class:`PendingGestureAction
        <poco.gesture.PendingGestureAction>` object which is able to generate decomposed gesture steps. You can invoke
        ``.to`` and ``.hold`` any times in a chain. See the following example.

        Examples:
            ::

                poco = Poco(...)

                # move from screen center to (0.6w, 0.6h) and hold for 1 second
                # then return back to center
                poco.start_gesture([0.5, 0.5]).to([0.6, 0.6]).hold(1).to([0.5, 0.5]).up()

        Args:
            pos: starting coordinate of normalized coordinate system

        Returns:
            :py:class:`PendingGestureAction <poco.gesture.PendingGestureAction>`: an object for building serialized
            gesture action.
        """

        return PendingGestureAction(self, pos)

    def apply_motion_tracks(self, tracks, accuracy=0.004):
        """
        Similar to click but press the screen for the given time interval and then release

        Args:
           tracks (:py:obj:`list`): list of :py:class:`poco.utils.track.MotionTrack` object
           accuracy (:py:obj:`float`): motion accuracy for each motion steps in normalized coordinate metrics.
        """

        if not tracks:
            raise ValueError('Please provide at least one track. Got {}'.format(repr(tracks)))

        tb = MotionTrackBatch(tracks)
        return self.agent.input.applyMotionEvents(tb.discretize(accuracy))

    def snapshot(self, width=720):
        """
        Take the screenshot from the target device. The supported output format (png, jpg, etc.) depends on the agent
        implementation.

        Args:
            width (:obj:`int`): an expected width of the screenshot. The real size depends on the agent implementation
            and might not be possible to obtain the expected width of the screenshot

        Returns:
            2-tuple:
                - screen_shot (:obj:`str/bytes`): base64 encoded screenshot data
                - format (:obj:`str`): output format 'png', 'jpg', etc.
        """

        return self.agent.screen.getScreen(width)

    def get_screen_size(self):
        """
        Get the real physical resolution of the screen of target device.

        Returns:
            tuple: float number indicating the screen physical resolution in pixels
        """

        return self.agent.screen.getPortSize()

    def command(self, cmd, type_=None):
        return self.agent.command.command(cmd, type_)

    def on_pre_action(self, action, ui, args):
        pass

    def on_post_action(self, action, ui, args):
        pass

    def add_pre_action_callback(self, cb):
        """
        Register a callback function to be invoked before each action (such as touch or swipe).

        The callback function arguments are defined as follows:

        * ``action`` (:obj:`str`): name or tag of the action
        * ``proxy`` (:py:class:`UIObjectProxy <poco.proxy.UIObjectProxy>` or :obj:`NoneType`): related UI proxy which is
          involved in the action itself
        * ``args`` (:obj:`tuple`): all required arguments of the specific action function

        Args:
            cb: the callback function
        """

        self._pre_action_callbacks.append(cb)

    def add_post_action_callback(self, cb):
        """
        Register a callback function to be invoked after each action (such as touch or swipe).

        The arguments to be passed are identical to the callback function in
        :py:meth:`add_pre_action_callback <poco.pocofw.Poco.add_pre_action_callback>`.

        Args:
            cb: the callback function
        """

        self._post_action_callbacks.append(cb)

    def pre_action(self, action, ui, args):
        for cb in self._pre_action_callbacks:
            try:
                cb(self, action, ui, args)
            except Exception as e:
                warnings.warn("Error occurred at pre action stage.\n{}".format(traceback.format_exc()))

    def post_action(self, action, ui, args):
        for cb in self._post_action_callbacks:
            try:
                cb(self, action, ui, args)
            except Exception as e:
                warnings.warn("Error occurred at post action stage.\n{}".format(traceback.format_exc()))

    def use_render_resolution(self, use=True, resolution=None):
        '''
        Whether to use render resolution

        Args:
            use: True or false
            resolution: render resolution in portrait mode, offset_x, offset_y, offset_width, offset_height, (0, 10, 1080, 1820)
        '''
        self._agent.input.use_render_resolution = use
        self._agent.input.render_resolution = resolution

    def dump(self):
        """
        Dump the current UI tree of the target device. The output format depends on the agent implementation.

        Returns:
            :obj:`str`: base64 encoded UI tree data
        """

        return self.agent.hierarchy.dump()
