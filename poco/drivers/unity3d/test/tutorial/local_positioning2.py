# coding=utf-8

import time
from poco.drivers.unity3d.test.tutorial.case import TutorialCase


class LocalPositioning1Tutorial(TutorialCase):
    def runTest(self):
        balloonfish_image = self.poco(text='balloonfish').focus([0.5, -3])
        balloonfish_image.long_click()
        time.sleep(0.2)


if __name__ == '__main__':
    import pocounit
    pocounit.main()
