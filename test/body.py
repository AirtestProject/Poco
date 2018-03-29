# coding=utf-8


import time
import json
from airtest_hunter import AirtestHunter, open_platform
from poco.drivers.netease.internal import NeteasePoco

from pocounit.case import PocoTestCase
from airtest.core.api import connect_device, device as current_device
from poco.drivers.android.uiautomation import AndroidUiautomationPoco


class Case(PocoTestCase):
    @classmethod
    def setUpClass(cls):
        super(Case, cls).setUpClass()
        if not current_device():
            connect_device('Android:///')

    def runTest(self):
        poco = AndroidUiautomationPoco()
        poco('com.sonyericsson.conversations:id/recipients_editor').set_text('\b\b\b')


if __name__ == '__main__':
    import pocounit
    pocounit.main()
