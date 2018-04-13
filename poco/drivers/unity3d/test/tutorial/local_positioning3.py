# coding=utf-8

import time
from poco.drivers.unity3d.test.tutorial.case import TutorialCase


class LocalPositioning1Tutorial(TutorialCase):
    def runTest(self):
        # focus is immutable
        fish = self.poco('fish').child(type='Image')
        fish_right_edge = fish.focus([1, 0.5])
        fish.long_click()  # still click the center
        time.sleep(0.2)
        fish_right_edge.long_click()  # will click the right edge
        time.sleep(0.2)


if __name__ == '__main__':
    import pocounit
    pocounit.main()
