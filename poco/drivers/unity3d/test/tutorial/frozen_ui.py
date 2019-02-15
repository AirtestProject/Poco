# coding=utf-8

import time
from poco.drivers.unity3d.test.tutorial.case import TutorialCase


class FrozenUITutorial(TutorialCase):
    def using_freezing(self):
        with self.poco.freeze() as frozen_poco:
            t0 = time.time()
            for item in frozen_poco('Scroll View').offspring(type='Text'):
                print(item.get_text())
            t1 = time.time()
            print(t1 - t0)

    def no_using_freezing(self):
        t0 = time.time()
        for item in self.poco('Scroll View').offspring(type='Text'):
            print(item.get_text())
        t1 = time.time()
        print(t1 - t0)

    def runTest(self):
        self.using_freezing()
        self.no_using_freezing()


if __name__ == '__main__':
    import pocounit
    pocounit.main()
