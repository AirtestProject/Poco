# coding=utf-8

import time
from pocounit.case import PocoTestCase
from pocounit.addons.poco.action_tracking import ActionTracker

from poco.drivers.unity3d import UnityPoco


class TutorialCase(PocoTestCase):
    @classmethod
    def setUpClass(cls):
        from airtest.core.api import connect_device
        connect_device('Android:///')

        cls.poco = UnityPoco()
        action_tracker = ActionTracker(cls.poco)
        cls.register_addon(action_tracker)

    @classmethod
    def tearDownClass(cls):
        time.sleep(1)
