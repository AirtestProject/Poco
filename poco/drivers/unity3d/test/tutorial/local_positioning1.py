# coding=utf-8

import time
from poco.drivers.unity3d.test.tutorial.case import TutorialCase


class LocalPositioning1Tutorial(TutorialCase):
    def runTest(self):
        image = self.poco('fish').child(type='Image')
        image.focus('center').long_click()
        time.sleep(0.2)
        image.focus([0.1, 0.1]).long_click()
        time.sleep(0.2)
        image.focus([0.9, 0.9]).long_click()
        time.sleep(0.2)
        image.focus([0.5, 0.9]).long_click()
        time.sleep(0.2)


if __name__ == '__main__':
    import pocounit
    pocounit.main()
