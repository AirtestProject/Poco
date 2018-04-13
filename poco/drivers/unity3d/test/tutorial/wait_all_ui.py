# coding=utf-8

import time
from poco.drivers.unity3d.test.tutorial.case import TutorialCase


class WaitAnyUITutorial(TutorialCase):
    def runTest(self):
        self.poco(text='wait UI 2').click()

        blue_fish = self.poco('fish_area').child('blue')
        yellow_fish = self.poco('fish_area').child('yellow')
        shark = self.poco('fish_area').child('black')

        self.poco.wait_for_all([blue_fish, yellow_fish, shark])
        self.poco('btn_back').click()
        time.sleep(2.5)


if __name__ == '__main__':
    import pocounit
    pocounit.main()
