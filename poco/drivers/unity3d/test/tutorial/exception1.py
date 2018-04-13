# coding=utf-8

import time
from poco.exceptions import InvalidOperationException
from poco.drivers.unity3d.test.tutorial.case import TutorialCase


class InvalidOperationExceptionTutorial(TutorialCase):
    def runTest(self):
        try:
            self.poco.click([1.1, 1.1])  # click outside screen
        except InvalidOperationException:
            print('oops')
            time.sleep(1)


if __name__ == '__main__':
    import pocounit
    pocounit.main()
