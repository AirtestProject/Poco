# coding=utf-8

from poco.drivers.unity3d.test.tutorial.case import TutorialCase


class ClickTutorial(TutorialCase):
    def runTest(self):
        self.poco('btn_start').click()


if __name__ == '__main__':
    from airtest.core.api import connect_device
    connect_device('Android:///')
    import pocounit
    pocounit.main()
