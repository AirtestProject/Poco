# coding=utf-8

from poco.drivers.unity3d.test.tutorial.case import TutorialCase


class DragTutorial(TutorialCase):
    def runTest(self):
        self.poco('star').drag_to(self.poco('shell'))


if __name__ == '__main__':
    import pocounit
    pocounit.main()
