# coding=utf-8

from poco.drivers.unity3d.test.tutorial.case import TutorialCase


class LongClickTutorial(TutorialCase):
    def runTest(self):
        self.poco('btn_start').click()
        self.poco('basic').click()
        self.poco('star_single').long_click()
        self.poco('star_single').long_click(duration=5)


if __name__ == '__main__':
    import pocounit
    pocounit.main()
