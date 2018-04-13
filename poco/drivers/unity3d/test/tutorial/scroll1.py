# coding=utf-8

from poco.drivers.unity3d.test.tutorial.case import TutorialCase


class Scroll1Tutorial(TutorialCase):
    def runTest(self):
        # swipe the list view up
        self.poco('Scroll View').swipe([0, -0.1])
        self.poco('Scroll View').swipe('up')  # the same as above, also have down/left/right
        self.poco('Scroll View').swipe('down')

        # perform swipe without UI selected
        x, y = self.poco('Scroll View').get_position()
        end = [x, y - 0.1]
        dir = [0, -0.1]
        self.poco.swipe([x, y], end)  # drag from point A to point B
        self.poco.swipe([x, y], direction=dir)  # drag from point A toward given direction and length


if __name__ == '__main__':
    import pocounit
    pocounit.main()
