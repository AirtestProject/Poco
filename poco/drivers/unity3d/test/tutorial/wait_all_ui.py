# coding=utf-8

import time
from poco.drivers.unity3d.test.tutorial.case import TutorialCase


class WaitAnyUITutorial(TutorialCase):
    def runTest(self):
        blue_fish = self.poco('fish_area').child('blue')
        yellow_fish = self.poco('fish_area').child('yellow')


        self.poco.wait_for_all([blue_fish, yellow_fish])
        self.poco.click('btn_back')
        time.sleep(2.5)


if __name__ == '__main__':
    from airtest.core.api import connect_device
    connect_device('Android:///')
    import pocounit
    pocounit.main()
