# coding=utf-8
__author__ = 'lxn3032'


import os
import time
import threading
import numbers
import warnings
import requests

from poco import Poco
from poco.exceptions import InvalidOperationException
from rpc import AndroidRpcClient

from airtest.core.android import Android, ADB
from airtest.core.android.ime_helper import YosemiteIme
from poco.vendor.android.utils.installation import install, uninstall


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

        # save current top activity
        current_top_activity_package = self.android.get_top_activity_name().split('/')[0]

        # install ime
        self.ime = YosemiteIme(self.android)
        self.ime.start()

        # install
        self._instrument_proc = None
        self._install_service()

        # forward
        p0, _ = self.adb_client.setup_forward("tcp:10080")
        p1, _ = self.adb_client.setup_forward("tcp:10081")

        # start
        if self._is_running('com.github.uiautomator'):
            warnings.warn('{} should not run together with "uiautomator". "uiautomator" will be killed.'
                          .format(self.__class__.__name__))
            self.adb_client.shell(['am', 'force-stop', 'com.github.uiautomator'])

        ready = self._start_instrument(p0)
        if not ready:
            # 启动失败则需要卸载再重启，instrument的奇怪之处
            uninstall(self.adb_client, PocoServicePackage)
            self._install_service()
            ready = self._start_instrument(p0)
            self.android.start_app(current_top_activity_package, activity=True)
            if not ready:
                raise RuntimeError("unable to launch AndroidUiautomationPoco")

        endpoint = "http://127.0.0.1:{}".format(p1)
        rpc_client = AndroidRpcClient(endpoint, self.ime)
        super(AndroidUiautomationPoco, self).__init__(rpc_client)

    def _install_service(self):
        updated = install(self.adb_client, os.path.join(this_dir, 'lib', 'pocoservice-debug.apk'))
        install(self.adb_client, os.path.join(this_dir, 'lib', 'pocoservice-debug-androidTest.apk'), updated)
        return updated

    def _is_running(self, package_name):
        processes = self.adb_client.shell(['ps']).splitlines()
        for ps in processes:
            ps = ps.strip()
            if ps.endswith(package_name):
                return True
        return False

    def _keep_running_instrumentation(self):
        def loop():
            while True:
                proc = self.adb_client.shell([
                    'am', 'instrument', '-w', '-e', 'class',
                    '{}.InstrumentedTestAsLauncher#launch'.format(PocoServicePackage),
                    '{}.test/android.support.test.runner.AndroidJUnitRunner'.format(PocoServicePackage)],
                    not_wait=True)
                stdout, stderr = proc.communicate()
                print(stdout)
                print(stderr)
                time.sleep(1)
        t = threading.Thread(target=loop)
        t.daemon = True
        t.start()

    def _start_instrument(self, port_to_ping):
        if self._instrument_proc is not None:
            self._instrument_proc.kill()
            self._instrument_proc = None
        ready = False
        self.adb_client.shell(['am', 'force-stop', PocoServicePackage])
        self._instrument_proc = self.adb_client.shell([
            'am', 'instrument', '-w', '-e', 'class',
            '{}.InstrumentedTestAsLauncher#launch'.format(PocoServicePackage),
            '{}.test/android.support.test.runner.AndroidJUnitRunner'.format(PocoServicePackage)],
            not_wait=True)
        time.sleep(2)
        for i in range(5):
            try:
                requests.get('http://127.0.0.1:{}'.format(port_to_ping), timeout=10)
                ready = True
                break
            except requests.exceptions.Timeout:
                break
            except requests.exceptions.ConnectionError:
                time.sleep(1)
                print("still waiting for uiautomation ready.")
                continue
        return ready

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


class AndroidUiautomationHelper(object):
    _nuis = {}

    @classmethod
    def get_instance(cls, serialno):
        if cls._nuis.get(serialno) is None:
            cls._nuis[serialno] = AndroidUiautomationPoco(serialno)
        return cls._nuis[serialno]
