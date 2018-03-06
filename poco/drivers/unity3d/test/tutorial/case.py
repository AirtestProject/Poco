# coding=utf-8


from pocounit.case import PocoTestCase
from pocounit.addons.poco.action_tracking import ActionTracker

from poco.drivers.unity3d import UnityPoco


class TutorialCase(PocoTestCase):
    @classmethod
    def setUpClass(cls):
        cls.poco = UnityPoco()
        action_tracker = ActionTracker(cls.poco)
        cls.register_addin(action_tracker)
