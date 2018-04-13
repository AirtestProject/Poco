# coding=utf-8

import time
from poco.exceptions import PocoNoSuchNodeException
from poco.drivers.unity3d.test.tutorial.case import TutorialCase


class InvalidOperationExceptionTutorial(TutorialCase):
    def runTest(self):
        node = self.poco('not existed node')  # select will never raise any exceptions
        try:
            node.click()
        except PocoNoSuchNodeException:
            print('oops!')
            time.sleep(1)

        try:
            node.attr('text')
        except PocoNoSuchNodeException:
            print('oops!')
            time.sleep(1)

        print(node.exists())  # => False. this method will not raise
        time.sleep(0.2)


if __name__ == '__main__':
    import pocounit
    pocounit.main()
