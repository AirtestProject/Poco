# coding=utf-8

import time
from poco.exceptions import PocoTargetTimeout
from poco.drivers.unity3d.test.tutorial.case import TutorialCase


class InvalidOperationExceptionTutorial(TutorialCase):
    def runTest(self):
        # UI is very slow
        self.poco('btn_start').click()
        star = self.poco('star')
        try:
            star.wait_for_appearance(timeout=3)  # wait until appearance within 3s
        except PocoTargetTimeout:
            print('oops!')
            time.sleep(1)


if __name__ == '__main__':
    import pocounit
    pocounit.main()
