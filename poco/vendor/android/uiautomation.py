# coding=utf-8
__author__ = 'lxn3032'


import os
import time
import threading
import warnings
import requests

from poco import Poco
from poco.agent import PocoAgent
from poco.vendor.android.rpc import AndroidHierarchy, AndroidScreen, AndroidInput

from airtest.core.android import Android
from airtest.core.android.ime import YosemiteIme
from poco.vendor.android.utils.installation import install, uninstall

from hrpc.client import RpcClient
from hrpc.transport.http import HttpTransport


this_dir = os.path.dirname(os.path.realpath(__file__))
PocoServicePackage = 'com.netease.open.pocoservice'
PocoServicePackageTest = 'com.netease.open.pocoservice.test'


class AndroidRpcClient(RpcClient):
    def __init__(self, endpoint):
        self.endpoint = endpoint
        super(AndroidRpcClient, self).__init__(HttpTransport)

    def initialize_transport(self):
        return HttpTransport(self.endpoint, self)


class AndroidPocoAgent(PocoAgent):
    def __init__(self, endpoint):
        self.client = AndroidRpcClient(endpoint)
        remote_poco = self.client.remote('poco-uiautomation-framework')
        dumper = remote_poco.dumper
        selector = remote_poco.selector
        attributor = remote_poco.attributor
        hierarchy = AndroidHierarchy(dumper, selector, attributor)
        screen = AndroidScreen(remote_poco.screen)
        inputer = AndroidInput(remote_poco.inputer)
        super(AndroidPocoAgent, self).__init__(hierarchy, inputer, screen, None)


class AndroidUiautomationPoco(Poco):
    def __init__(self, device=None):
        # TODO: 临时用着airtest的方案
        self.android = device or Android()
        self.adb_client = self.android.adb

        # save current top activity (@nullable)
        current_top_activity_package = self.android.get_top_activity_name()
        if current_top_activity_package is not None:
            current_top_activity_package = current_top_activity_package.split('/')[0]

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

            current_top_activity2 = self.android.get_top_activity_name()
            if current_top_activity2 is None or current_top_activity_package not in current_top_activity2:
                self.android.start_app(current_top_activity_package, activity=True)

            if not ready:
                raise RuntimeError("unable to launch AndroidUiautomationPoco")

        endpoint = "http://{}:{}".format(self.adb_client.host, p1)
        agent = AndroidPocoAgent(endpoint)
        super(AndroidUiautomationPoco, self).__init__(agent)

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
                requests.get('http://{}:{}'.format(self.adb_client.host, port_to_ping), timeout=10)
                ready = True
                break
            except requests.exceptions.Timeout:
                break
            except requests.exceptions.ConnectionError:
                time.sleep(1)
                print("still waiting for uiautomation ready.")
                continue
        return ready


class AndroidUiautomationHelper(object):
    _nuis = {}

    @classmethod
    def get_instance(cls, device):
        if cls._nuis.get(device) is None:
            cls._nuis[device] = AndroidUiautomationPoco(device)
        return cls._nuis[device]
