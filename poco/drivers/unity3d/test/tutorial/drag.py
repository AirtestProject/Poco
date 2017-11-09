# coding=utf-8

from poco.drivers.unity3d.test.tutorial.case import TutorialCase


class DragTutorial(TutorialCase):
    def runTest(self):
        shell = self.poco('shell')
        for star in self.poco('star'):
            star.drag_to(shell)


if __name__ == '__main__':
    from airtest.core.api import connect_device
    connect_device('Android:///')
    import pocounit
    pocounit.main()
