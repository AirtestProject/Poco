# coding=utf-8

import base64
import json
import traceback
import time
import unittest

from poco.drivers.std import StdPoco
from poco.utils.simplerpc.utils import sync_wrapper, RemoteError
from airtest.core.api import connect_device


class TestStandardFunction(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # u3d game 默认5001
        # cocos2dx-lua 默认15004
        connect_device('Android:///')
        # connect_device('Windows:///?class_name=UnityWndClass&title_re=Unity.*')
        cls.poco = StdPoco(15004)

    @classmethod
    def tearDownClass(cls):
        time.sleep(1)

    def test_dump(self):
        h = self.poco.agent.hierarchy.dump()
        s = json.dumps(h, indent=4)
        print(s)
        self.assertNotIn('"visible": false', s)

    def test_dump_include_invisible_node(self):
        h = self.poco.agent.hierarchy.dumper.dumpHierarchy(onlyVisibleNode=False)  # .hierarchy是FrozenUIHierarchy
        s = json.dumps(h, indent=4)
        print(s)
        self.assertIn('"visible": false', s)

    def test_getSdkVersion(self):
        print(self.poco.agent.get_sdk_version())

    def test_no_such_rpc_method(self):
        @sync_wrapper
        def wrapped(*args, **kwargs):
            return self.poco.agent.c.call('no_such_method')

        with self.assertRaises(RemoteError):
            wrapped()
        try:
            wrapped()
        except:
            traceback.print_exc()

    def test_get_screen(self):
        b64img, fmt = self.poco.snapshot()
        with open('screen.{}'.format(fmt), 'wb') as f:
            f.write(base64.b64decode(b64img))

    def test_get_screen_size(self):
        print(self.poco.get_screen_size())

    def test_motion_events(self):
        ui = self.poco()[0]
        ui.click()
        time.sleep(0.5)
        ui.long_click()
        time.sleep(0.5)
        ui.swipe([0.1, 0.1])

    def test_set_text(self):
        textval = 'hello 中国!'
        node = self.poco(typeMatches='TextField|InputField|EditBox')
        node.set_text(textval)
        node.invalidate()
        actualVal = node.get_text() or node.offspring(text=textval).get_text()
        print(repr(actualVal))
        self.assertEqual(actualVal, textval)

    def test_clear_text(self):
        node = self.poco(typeMatches='TextField|InputField|EditBox')
        node.set_text('val2333')
        node.set_text('')
        node.invalidate()
        actual_val = node.get_text()
        if actual_val is None:
            actual_val = node.offspring(text='').get_text()
        self.assertEqual(actual_val, '')

    def test_instanceId(self):
        for n in self.poco():
            instance_id = n.attr('_instanceId')
            if instance_id:
                print(instance_id)
