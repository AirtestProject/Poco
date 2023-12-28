# coding=utf-8
__author__ = 'lxn3032'


import os
import requests
import time
import warnings
import threading
import atexit

from airtest.core.android.ime import YosemiteIme
from airtest.core.error import AdbShellError, AirtestError

from hrpc.client import RpcClient
from hrpc.transport.http import HttpTransport
from poco.pocofw import Poco
from poco.agent import PocoAgent
from poco.sdk.Attributor import Attributor
from poco.sdk.interfaces.screen import ScreenInterface
from poco.utils.hrpc.hierarchy import RemotePocoHierarchy
from poco.utils.airtest.input import AirtestInput
from poco.utils import six
from poco.utils.device import default_device
from poco.drivers.android.utils.installation import install, uninstall

__all__ = ['AndroidUiautomationPoco', 'AndroidUiautomationHelper']
this_dir = os.path.dirname(os.path.realpath(__file__))
PocoServicePackage = 'com.netease.open.pocoservice'
PocoServicePackageTest = 'com.netease.open.pocoservice.test'
UiAutomatorPackage = 'com.github.uiautomator'


class AndroidRpcClient(RpcClient):
    def __init__(self, endpoint):
        self.endpoint = endpoint
        super(AndroidRpcClient, self).__init__(HttpTransport)

    def initialize_transport(self):
        return HttpTransport(self.endpoint, self)


# deprecated
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
        if attrName == 'text' and attrVal != '':
            # 先清除了再设置，虽然这样不如直接用ime的方法好，但是也能凑合用着
            current_val = self.remote.getAttr(node, 'text')
            if current_val:
                self.remote.setAttr(node, 'text', '')
            self.ime.text(attrVal)
        else:
            self.remote.setAttr(node, attrName, attrVal)


class ScreenWrapper(ScreenInterface):
    def __init__(self, screen):
        super(ScreenWrapper, self).__init__()
        self.screen = screen

    def getScreen(self, width):
        # Android上PocoService的实现为仅返回b64编码的图像，格式固定位jpg
        b64img = self.screen.getScreen(width)
        return b64img, 'jpg'

    def getPortSize(self):
        return self.screen.getPortSize()


class AndroidPocoAgent(PocoAgent):
    def __init__(self, endpoint, ime, use_airtest_input=False):
        self.client = AndroidRpcClient(endpoint)
        remote_poco = self.client.remote('poco-uiautomation-framework')
        dumper = remote_poco.dumper
        selector = remote_poco.selector
        attributor = remote_poco.attributor
        hierarchy = RemotePocoHierarchy(dumper, selector, attributor)

        if use_airtest_input:
            inputer = AirtestInput()
        else:
            inputer = remote_poco.inputer
        super(AndroidPocoAgent, self).__init__(hierarchy, inputer, ScreenWrapper(remote_poco.screen), None)


class KeepRunningInstrumentationThread(threading.Thread):
    """Keep pocoservice running"""

    def __init__(self, poco, port_to_ping):
        super(KeepRunningInstrumentationThread, self).__init__()
        self._stop_event = threading.Event()
        self.poco = poco
        self.port_to_ping = port_to_ping
        self.daemon = True

    def stop(self):
        self._stop_event.set()

    def stopped(self):
        return self._stop_event.is_set()

    def run(self):
        while not self.stopped():
            if not self.stopped():
                self.poco._start_instrument(self.port_to_ping)  # 尝试重启
                time.sleep(1)


class AndroidUiautomationPoco(Poco):
    """
    Poco Android implementation for testing **Android native apps**.

    Args:
        device (:py:obj:`Device`): :py:obj:`airtest.core.device.Device` instance provided by ``airtest``. leave the 
         parameter default and the default device will be chosen. more details refer to ``airtest doc``
        using_proxy (:py:obj:`bool`): whether use adb forward to connect the Android device or not
        force_restart (:py:obj:`bool`): whether always restart the poco-service-demo running on Android device or not
        options: see :py:class:`poco.pocofw.Poco`

    Examples:
        The simplest way to initialize AndroidUiautomationPoco instance and no matter your device network status::

            from poco.drivers.android.uiautomation import AndroidUiautomationPoco

            poco = AndroidUiautomationPoco()
            poco('android:id/title').click()
            ...

    """

    def __init__(self, device=None, using_proxy=True, force_restart=False, use_airtest_input=False, **options):
        # 加这个参数为了不在最新的pocounit方案中每步都截图
        self.screenshot_each_action = True
        if options.get('screenshot_each_action') is False:
            self.screenshot_each_action = False

        self.device = device or default_device()

        self.adb_client = self.device.adb
        if using_proxy:
            self.device_ip = self.adb_client.host or "127.0.0.1"
        else:
            self.device_ip = self.device.get_ip_address()

        # save current top activity (@nullable)
        try:
            current_top_activity_package = self.device.get_top_activity_name()
        except AirtestError as e:
            # 在一些极端情况下，可能获取不到top activity的信息
            print(e)
            current_top_activity_package = None
        if current_top_activity_package is not None:
            current_top_activity_package = current_top_activity_package.split('/')[0]

        # install ime
        self.ime = YosemiteIme(self.adb_client)

        # install
        self._instrument_proc = None
        self._install_service()

        # forward
        self.forward_list = []
        if using_proxy:
            p0, _ = self.adb_client.setup_forward("tcp:10080")
            p1, _ = self.adb_client.setup_forward("tcp:10081")
            self.forward_list.extend(["tcp:%s" % p0, "tcp:%s" % p1])
        else:
            p0 = 10080
            p1 = 10081

        # start
        ready = self._start_instrument(p0, force_restart=force_restart)
        if not ready:
            # 之前启动失败就卸载重装，现在改为尝试kill进程或卸载uiautomator
            self._kill_uiautomator()
            ready = self._start_instrument(p0)

            if current_top_activity_package is not None:
                current_top_activity2 = self.device.get_top_activity_name()
                if current_top_activity2 is None or current_top_activity_package not in current_top_activity2:
                    self.device.start_app(current_top_activity_package, activity=True)

            if not ready:
                raise RuntimeError("unable to launch AndroidUiautomationPoco")
        if ready:
            # 首次启动成功后，在后台线程里监控这个进程的状态，保持让它不退出
            self._keep_running_thread = KeepRunningInstrumentationThread(self, p0)
            self._keep_running_thread.start()

        endpoint = "http://{}:{}".format(self.device_ip, p1)
        agent = AndroidPocoAgent(endpoint, self.ime, use_airtest_input)
        super(AndroidUiautomationPoco, self).__init__(agent, **options)

    def _install_service(self):
        updated = install(self.adb_client, os.path.join(this_dir, 'lib', 'pocoservice-debug.apk'))
        return updated

    def _is_running(self, package_name):
        """
        use ps |grep to check whether the process exists

        :param package_name: package name(e.g., com.github.uiautomator)
                            or regular expression(e.g., poco\|airtest\|uiautomator\|airbase)
        :return: pid or None
        """
        cmd = r' |echo $(grep -E {package_name})'.format(package_name=package_name)
        if self.device.sdk_version > 25:
            cmd = r'ps -A' + cmd
        else:
            cmd = r'ps' + cmd
        processes = self.adb_client.shell(cmd).splitlines()
        for ps in processes:
            if ps:
                ps = ps.split()
                return ps[1]
        return None

    def _start_instrument(self, port_to_ping, force_restart=False):
        if not force_restart:
            try:
                state = requests.get('http://{}:{}/uiautomation/connectionState'.format(self.device_ip, port_to_ping),
                                     timeout=10)
                state = state.json()
                if state.get('connected'):
                    # skip starting instrumentation if UiAutomation Service already connected.
                    return True
            except:
                pass

        if self._instrument_proc is not None:
            if self._instrument_proc.poll() is None:
                self._instrument_proc.kill()
            self._instrument_proc = None

        ready = False
        # self.adb_client.shell(['am', 'force-stop', PocoServicePackage])

        # 启动instrument之前，先把主类activity启动起来，不然instrumentation可能失败
        self.adb_client.shell('am start -n {}/.TestActivity'.format(PocoServicePackage))

        instrumentation_cmd = [
            'am', 'instrument', '-w', '-e', 'debug', 'false', '-e', 'class',
            '{}.InstrumentedTestAsLauncher'.format(PocoServicePackage),
            '{}/androidx.test.runner.AndroidJUnitRunner'.format(PocoServicePackage)]
        self._instrument_proc = self.adb_client.start_shell(instrumentation_cmd)

        def cleanup_proc(proc):
            def wrapped():
                try:
                    proc.kill()
                except:
                    pass
            return wrapped
        atexit.register(cleanup_proc(self._instrument_proc))

        time.sleep(2)
        for i in range(10):
            try:
                requests.get('http://{}:{}'.format(self.device_ip, port_to_ping), timeout=10)
                ready = True
                break
            except requests.exceptions.Timeout:
                break
            except requests.exceptions.ConnectionError:
                if self._instrument_proc.poll() is not None:
                    warnings.warn("[pocoservice.apk] instrumentation test server process is no longer alive")
                    stdout = self._instrument_proc.stdout.read()
                    stderr = self._instrument_proc.stderr.read()
                    print('[pocoservice.apk] stdout: {}'.format(stdout))
                    print('[pocoservice.apk] stderr: {}'.format(stderr))
                time.sleep(1)
                print("still waiting for uiautomation ready.")
                try:
                    self.adb_client.shell(
                        ['monkey', '-p', {PocoServicePackage}, '-c', 'android.intent.category.LAUNCHER', '1'])
                except Exception as e:
                    pass
                self.adb_client.shell('am start -n {}/.TestActivity'.format(PocoServicePackage))
                instrumentation_cmd = [
                    'am', 'instrument', '-w', '-e', 'debug', 'false', '-e', 'class',
                    '{}.InstrumentedTestAsLauncher'.format(PocoServicePackage),
                    '{}/androidx.test.runner.AndroidJUnitRunner'.format(PocoServicePackage)]
                self._instrument_proc = self.adb_client.start_shell(instrumentation_cmd)
                continue
        return ready

    def _kill_uiautomator(self):
        """
        poco-service无法与其他instrument启动的apk同时存在，因此在启动前，需要杀掉一些可能的进程：
        比如 io.appium.uiautomator2.server, com.github.uiautomator, com.netease.open.pocoservice等

        :return:
        """
        pid = self._is_running("uiautomator")
        if pid:
            warnings.warn('{} should not run together with "uiautomator". "uiautomator" will be killed.'
                          .format(self.__class__.__name__))
            self.adb_client.shell(['am', 'force-stop', PocoServicePackage])

            try:
                self.adb_client.shell(['kill', pid])
            except AdbShellError:
                # 没有root权限
                uninstall(self.adb_client, UiAutomatorPackage)

    def on_pre_action(self, action, ui, args):
        if self.screenshot_each_action:
            # airteset log用
            from airtest.core.api import snapshot
            msg = repr(ui)
            if not isinstance(msg, six.text_type):
                msg = msg.decode('utf-8')
            snapshot(msg=msg)

    def stop_running(self):
        print('[pocoservice.apk] stopping PocoService')
        self._keep_running_thread.stop()
        self._keep_running_thread.join(3)
        self.remove_forwards()
        self.adb_client.shell(['am', 'force-stop', PocoServicePackage])

    def remove_forwards(self):
        for p in self.forward_list:
            self.adb_client.remove_forward(p)
        self.forward_list = []


class AndroidUiautomationHelper(object):
    _nuis = {}

    @classmethod
    def get_instance(cls, device):
        """
        This is only a slot to store and get already initialized poco instance rather than initializing again. You can
        simply pass the ``current device instance`` provided by ``airtest`` to get the AndroidUiautomationPoco instance.
        If no such AndroidUiautomationPoco instance, a new instance will be created and stored. 

        Args:
            device (:py:obj:`airtest.core.device.Device`): more details refer to ``airtest doc``

        Returns:
            poco instance
        """

        if cls._nuis.get(device) is None:
            cls._nuis[device] = AndroidUiautomationPoco(device)
        return cls._nuis[device]
