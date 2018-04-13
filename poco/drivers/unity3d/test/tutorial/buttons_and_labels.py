# coding=utf-8

import time
from poco.drivers.unity3d.test.tutorial.case import TutorialCase


class ButtonsAndLabelsTutorial(TutorialCase):
    def runTest(self):
        self.poco('btn_start').click()
        self.poco(text='basic').click()

        star = self.poco('star_single')
        if star.exists():
            pos = star.get_position()
            input_field = self.poco('pos_input')
            time.sleep(1)
            input_field.set_text('x={:.02f}, y={:.02f}'.format(*pos))
            time.sleep(3)

        title = self.poco('title').get_text()
        if title == 'Basic test':
            self.poco('btn_back', type='Button').click()
            self.poco('btn_back', type='Button').click()


if __name__ == '__main__':
    import pocounit
    pocounit.main()
