# coding=utf-8
__author__ = 'lxn3032'


import os
import time
import numbers
import warnings
import requests

from poco import Poco
from poco.exceptions import InvalidOperationException
from rpc import AndroidRpcClient

from airtest.core.android import Android, ADB
from airtest.core.android.ime_helper import YosemiteIme
from poco.vendor.android.utils.installation import install


this_dir = os.path.dirname(os.path.realpath(__file__))
PocoServicePackage = 'com.netease.open.pocoservice'
PocoServicePackageTest = 'com.netease.open.pocoservice.test'


class AndroidUiautomationPoco(Poco):
    def __init__(self, serial=None):
        # TODO: 临时用着airtest的方案
        self.android = Android(serial, init_display=False, minicap=False, minicap_stream=False, minitouch=False, shell_ime=False)
        self.adb_client = self.android.adb
        if not serial:
            devices = self.adb_client.devices("device")
            if len(devices) == 0:
                raise RuntimeError('No available device connected. Please check your adb connection.')
            elif len(devices) > 1:
                raise RuntimeError('Too much devices connected. Please specified one by serialno.')
            self.adb_client.set_serialno(devices[0][0])

        # install ime
        self.ime = YosemiteIme(self.android)
        self.ime.start()

        # install
        updated = install(self.adb_client, os.path.join(this_dir, 'lib', 'pocoservice-debug.apk'))
        install(self.adb_client, os.path.join(this_dir, 'lib', 'pocoservice-debug-androidTest.apk'), updated)

        # forward
        p0, _ = self.adb_client.setup_forward("tcp:10080")
        p1, _ = self.adb_client.setup_forward("tcp:10081")

        # start
        if updated:
            self.adb_client.shell(['am', 'force-stop', PocoServicePackage])

        if self._is_running('com.github.uiautomator'):
            warnings.warn('{} should not run together with "uiautomator". "uiautomator" will be killed.'
                          .format(self.__class__.__name__))
            self.adb_client.shell(['am', 'force-stop', 'com.github.uiautomator'])
        self.adb_client.shell([
            'am', 'instrument', '-w', '-e', 'class',
            '{}.InstrumentedTestAsLauncher#launch'.format(PocoServicePackage),
            '{}.test/android.support.test.runner.AndroidJUnitRunner'.format(PocoServicePackage)],
            not_wait=True)
        time.sleep(2)
        self._wait_for_remote_ready(p0)
        time.sleep(1)

        endpoint = "http://127.0.0.1:{}".format(p1)
        rpc_client = AndroidRpcClient(endpoint, self.ime)
        super(AndroidUiautomationPoco, self).__init__(rpc_client)

    def _is_running(self, package_name):
        processes = self.adb_client.shell(['ps']).splitlines()
        for ps in processes:
            ps = ps.strip()
            if ps.endswith(package_name):
                return True
        return False

    @staticmethod
    def _wait_for_remote_ready(port):
        for i in range(10):
            try:
                requests.get('http://127.0.0.1:{}'.format(port), timeout=20)
            except requests.exceptions.Timeout:
                raise RuntimeError("unable to launch AndroidUiautomationPoco")
            except requests.exceptions.ConnectionError:
                time.sleep(1)
                print("still waiting for uiautomation ready.")
                continue
            break

    def click(self, pos):
        if not (0 <= pos[0] <= 1) or not (0 <= pos[1] <= 1):
            raise InvalidOperationException('Click position out of screen. {}'.format(pos))
        self.rpc.click(*pos)

    def swipe(self, p1, p2=None, direction=None, duration=1.0):
        if not (0 <= p1[0] <= 1) or not (0 <= p1[1] <= 1):
            raise InvalidOperationException('Swipe origin out of screen. {}'.format(p1))
        if p2:
            sp2 = p2
        elif direction:
            sp2 = [p1[0] + direction[0], p1[1] + direction[1]]
        else:
            raise RuntimeError("p2 and direction cannot be None at the same time.")
        self.rpc.swipe(p1[0], p1[1], sp2[0], sp2[1], duration)

    def long_click(self, pos, duration=3.0):
        if not (0 <= pos[0] <= 1) or not (0 <= pos[1] <= 1):
            raise InvalidOperationException('Click position out of screen. {}'.format(pos))
        self.rpc.long_click(pos[0], pos[1], duration)

    def get_screen_size(self):
        return self.rpc.get_screen_size()

    def snapshot(self, width=720):
        # snapshot接口暂时还补统一
        if not isinstance(width, numbers.Number):
            return None

        return self.rpc.get_screen(int(width))
