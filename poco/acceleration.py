# coding=utf-8
from __future__ import unicode_literals

import time
import warnings

from poco.exceptions import PocoTargetTimeout

__author__ = 'lxn3032'


class PocoAccelerationMixin(object):
    """
    This class provides some high-level method to reduce redundant code implementations.
    As this is a MixinClass, please do not introduce new state in methods.
    """

    def dismiss(self, targets, exit_when=None, sleep_interval=0.5, appearance_timeout=20, timeout=120):
        """
        Automatically dismiss the target objects

        Args:
            targets (:obj:`list`): list of poco objects to be dropped
            exit_when: termination condition, default is None which means to automatically exit when list of
             ``targets`` is empty
            sleep_interval: time interval between each actions for the given targets, default is 0.5s
            appearance_timeout: time interval to wait for given target to appear on the screen, automatically exit when
             timeout, default is 20s
            timeout: dismiss function timeout, default is 120s

        Raises:
            PocoTargetTimeout: when dismiss time interval timeout, under normal circumstances, this should not happen
             and if happens, it will be reported
        """

        try:
            self.wait_for_any(targets, timeout=appearance_timeout)
        except PocoTargetTimeout:
            # here returns only when timeout
            # 仅当超时时自动退出
            warnings.warn('Waiting timeout when trying to dismiss something before them appear. Targets are {}'
                          .encode('utf-8').format(targets))
            return

        start_time = time.time()
        while True:
            no_target = True
            for t in targets:
                if t.exists():
                    try:
                        for n in t:
                            try:
                                n.click(sleep_interval=sleep_interval)
                                no_target = False
                            except:
                                pass
                    except:
                        # Catch the NodeHasBeenRemoved exception if some node was removed over the above iteration
                        # and just ignore as this will not affect the result.
                        # 遍历(__iter__: for n in t)过程中如果节点正好被移除了，可能会报远程节点被移除的异常
                        # 这个报错忽略就行
                        pass
            time.sleep(sleep_interval)
            should_exit = exit_when() if exit_when else False
            if no_target or should_exit:
                return

            if time.time() - start_time > timeout:
                raise PocoTargetTimeout('dismiss', targets)
