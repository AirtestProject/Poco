# coding=utf-8
__author__ = 'lxn3032'


import os
import requests
import time
import warnings

try:
    new_airtest_api = True
    import airtest.core.api as _____
except ImportError:
    new_airtest_api = False
    from airtest.core.android.utils.iputils import get_ip_address

from airtest.core.android.ime import YosemiteIme


from hrpc.client import RpcClient
from hrpc.transport.http import HttpTransport
from poco import Poco
from poco.agent import PocoAgent
from poco.sdk.Attributor import Attributor
from poco.utils.hrpc.hierarchy import RemotePocoHierarchy
from poco.drivers.android.utils.installation import install, uninstall

__all__ = ['AndroidUiautomationPoco', 'AndroidUiautomationHelper']
this_dir = os.path.dirname(os.path.realpath(__file__))
PocoServicePackage = 'com.netease.open.pocoservice'
PocoServicePackageTest = 'com.netease.open.pocoservice.test'


class AndroidRpcClient(RpcClient):
    def __init__(self, endpoint):
        self.endpoint = endpoint
        super(AndroidRpcClient, self).__init__(HttpTransport)

    def initialize_transport(self):
        return HttpTransport(self.endpoint, self)


class AttributorWrapper(Attributor):
    """
    部分手机上仍不支持Accessibility.ACTION_SET_TEXT，使用YosemiteIme还是兼容性最好的方案
    这个class会hook住set_text，然后改用ime的text方法
    """

    def __init__(self, remote, ime):
        self.remote = remote
        self.ime = ime

    def getAttr(self, node, attrName):
        return self.remote.getAttr(node, attrName)

    def setAttr(self, node, attrName, attrVal):
        if attrName == 'text':
            self.ime.text(attrVal)
        else:
            self.remote.setAttr(node, attrName, attrVal)


class AndroidPocoAgent(PocoAgent):
    def __init__(self, endpoint, ime):
        self.client = AndroidRpcClient(endpoint)
        remote_poco = self.client.remote('poco-uiautomation-framework')
        dumper = remote_poco.dumper
        selector = remote_poco.selector
        attributor = AttributorWrapper(remote_poco.attributor, ime)
        hierarchy = RemotePocoHierarchy(dumper, selector, attributor)
        super(AndroidPocoAgent, self).__init__(hierarchy, remote_poco.inputer, remote_poco.screen, None)


class AndroidUiautomationPoco(Poco):
    def __init__(self, device=None, using_proxy=True, **options):
        if not device:
            try:
                # new version
                from airtest.core.api import connect_device, device as current_device
                if not current_device():
                    connect_device("Android:///")
            except ImportError:
                # old version
                from airtest.cli.runner import device as current_device
                from airtest.core.main import set_serialno
                if not current_device():
                    set_serialno()
            self.android = current_device()
        else:
            self.android = device
        self.adb_client = self.android.adb
        if using_proxy:
            self.device_ip = self.adb_client.host or "127.0.0.1"
        else:
            if new_airtest_api:
                self.device_ip = self.adb_client.get_ip_address()
            else:
                self.device_ip = get_ip_address(self.adb_client)

        # save current top activity (@nullable)
        current_top_activity_package = self.android.get_top_activity_name()
        if current_top_activity_package is not None:
            current_top_activity_package = current_top_activity_package.split('/')[0]

        # install ime
        self.ime = YosemiteIme(self.adb_client)
        self.ime.start()

        # install
        self._instrument_proc = None
        self._install_service()

        # forward
        if using_proxy:
            p0, _ = self.adb_client.setup_forward("tcp:10080")
            p1, _ = self.adb_client.setup_forward("tcp:10081")
        else:
            p0 = 10080
            p1 = 10081

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

            if current_top_activity_package is not None:
                current_top_activity2 = self.android.get_top_activity_name()
                if current_top_activity2 is None or current_top_activity_package not in current_top_activity2:
                    self.android.start_app(current_top_activity_package, activity=True)

            if not ready:
                raise RuntimeError("unable to launch AndroidUiautomationPoco")

        endpoint = "http://{}:{}".format(self.device_ip, p1)
        agent = AndroidPocoAgent(endpoint, self.ime)
        super(AndroidUiautomationPoco, self).__init__(agent, **options)

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

    # def _keep_running_instrumentation(self):
    #     def loop():
    #         while True:
    #             proc = self.adb_client.shell([
    #                 'am', 'instrument', '-w', '-e', 'class',
    #                 '{}.InstrumentedTestAsLauncher#launch'.format(PocoServicePackage),
    #                 '{}.test/android.support.test.runner.AndroidJUnitRunner'.format(PocoServicePackage)],
    #                 not_wait=True)
    #             stdout, stderr = proc.communicate()
    #             print(stdout)
    #             print(stderr)
    #             time.sleep(1)
    #     t = threading.Thread(target=loop)
    #     t.daemon = True
    #     t.start()

    def _start_instrument(self, port_to_ping):
        if self._instrument_proc is not None:
            self._instrument_proc.kill()
            self._instrument_proc = None
        ready = False
        self.adb_client.shell(['am', 'force-stop', PocoServicePackage])

        # 启动instrument之前，先把主类activity启动起来，不然instrumentation可能失败
        self.adb_client.shell('am start -n {}/.TestActivity'.format(PocoServicePackage))

        instrumentation_cmd = [
                'am', 'instrument', '-w', '-e', 'debug', 'false', '-e', 'class',
                '{}.InstrumentedTestAsLauncher'.format(PocoServicePackage),
                '{}.test/android.support.test.runner.AndroidJUnitRunner'.format(PocoServicePackage)]
        if new_airtest_api:
            self._instrument_proc = self.adb_client.start_shell(instrumentation_cmd)
        else:
            self._instrument_proc = self.adb_client.shell(instrumentation_cmd, not_wait=True)
        time.sleep(2)
        for i in range(10):
            try:
                requests.get('http://{}:{}'.format(self.device_ip, port_to_ping), timeout=10)
                ready = True
                break
            except requests.exceptions.Timeout:
                break
            except requests.exceptions.ConnectionError:
                time.sleep(1)
                print("still waiting for uiautomation ready.")
                continue
        return ready

    def on_pre_action(self, action, proxy, args):
        # airteset log用
        try:
            from airtest.core.api import snapshot
        except ImportError:
            # 兼容旧airtest
            from airtest.core.main import snapshot
        snapshot(msg=unicode(proxy))


class AndroidUiautomationHelper(object):
    _nuis = {}

    @classmethod
    def get_instance(cls, device):
        if cls._nuis.get(device) is None:
            cls._nuis[device] = AndroidUiautomationPoco(device)
        return cls._nuis[device]
