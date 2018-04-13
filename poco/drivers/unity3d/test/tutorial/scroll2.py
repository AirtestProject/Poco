# coding=utf-8

import time
from poco.drivers.unity3d.test.tutorial.case import TutorialCase


class Scroll2Tutorial(TutorialCase):
    def runTest(self):
        listView = self.poco('Scroll View')
        listView.focus([0.5, 0.8]).drag_to(listView.focus([0.5, 0.2]))
        time.sleep(1)


if __name__ == '__main__':
    import pocounit
    pocounit.main()
