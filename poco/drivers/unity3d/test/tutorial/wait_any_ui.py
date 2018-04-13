# coding=utf-8

import time
from poco.drivers.unity3d.test.tutorial.case import TutorialCase


class WaitAnyUITutorial(TutorialCase):
    def runTest(self):
        self.poco(text='wait UI').click()

        bomb_count = 0
        while True:
            blue_fish = self.poco('fish_emitter').child('blue')
            yellow_fish = self.poco('fish_emitter').child('yellow')
            bomb = self.poco('fish_emitter').child('bomb')
            fish = self.poco.wait_for_any([blue_fish, yellow_fish, bomb])
            if fish is bomb:
                bomb_count += 1
                if bomb_count > 3:
                    return
            else:
                fish.click()
            time.sleep(2.5)


if __name__ == '__main__':
    import pocounit
    pocounit.main()
