# coding=utf-8

import time
from poco.drivers.unity3d.test.tutorial.case import TutorialCase


class OverviewTutorial(TutorialCase):
    def runTest(self):
        self.poco('btn_start').click()
        time.sleep(1)

        self.poco(textMatches='drag.*').click()
        time.sleep(1)

        shell = self.poco('shell').focus('center')
        for star in self.poco('star'):
            star.drag_to(shell)
        time.sleep(1)

        self.assertEqual(self.poco('scoreVal').get_text(), "100", "score correct.")
        self.poco('btn_back', type='Button').click()

    def tearDown(self):
        time.sleep(2)


if __name__ == '__main__':
    import pocounit
    pocounit.main()
