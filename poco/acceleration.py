# coding=utf-8
__author__ = 'lxn3032'


import time


class PocoUIAccelerationMixin(object):
    def auto_dismiss(self, targets, exit_when=None, click_anchor=True, sleep_interval=1, appearance_timeout=20):
        try:
            self.wait_for_any(targets, timeout=appearance_timeout)
        except:
            return
        while True:
            no_target = True
            for t in targets:
                if t.exists():
                    try:
                        t.click(click_anchor=click_anchor, sleep_interval=sleep_interval)
                        no_target = False
                    except:
                        pass
            time.sleep(sleep_interval)
            should_exit = exit_when() if exit_when else False
            if no_target or should_exit:
                return
