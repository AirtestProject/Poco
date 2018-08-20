# coding=utf-8

import time
import base64
import zlib
import re
import pyautogui
import atomac
import operator
from poco.sdk.std.rpc.controller import StdRpcEndpointController
from poco.sdk.std.rpc.reactor import StdRpcReactor
from poco.utils.net.transport.tcp import TcpSocket
from poco.drivers.osx.sdk.OSXUIDumper import OSXUIDumper
from poco.sdk.exceptions import UnableToSetAttributeException, NonuniqueSurfaceException, InvalidSurfaceException
from poco.utils.six import string_types, PY2
from poco.utils.six.moves import reduce
from poco.drivers.osx.sdk.OSXUIFunc import OSXFunc

DEFAULT_PORT = 15004
DEFAULT_ADDR = ('0.0.0.0', DEFAULT_PORT)


class PocoSDKOSX(object):

    def __init__(self, addr=DEFAULT_ADDR):
        self.addr = addr
        self.running = False
        self.root = None

    def Dump(self, _):
        res = OSXUIDumper(self.root).dumpHierarchy()
        return res

    def SetForeground(self):
        self.root.AXMinimized = False
        self.app.AXFrontmost = True

    def GetSDKVersion(self):
        return '0.0.1'

    def GetDebugProfilingData(self):
        return {}

    def GetScreenSize(self):
        Width = self.root.AXSize[0]
        Height = self.root.AXSize[1]
        return [Width, Height]

    def GetWindowRect(self):
        Width = self.root.AXSize[0]
        Height = self.root.AXSize[1]
        return [self.root.AXPosition[0], self.root.AXPosition[1], self.root.AXPosition[0] + Width, self.root.AXPosition[1] + Height]

    def Screenshot(self, width):
        self.SetForeground()
        size = self.root.AXSize
        pos = self.root.AXPosition
        pyautogui.screenshot('Screenshot.png', (pos[0], pos[1], size[0], size[1])).save('Screenshot.png')
        f = open(r'Screenshot.png', 'rb')
        deflated = zlib.compress(f.read())
        ls_f = base64.b64encode(deflated)
        f.close()
        return [ls_f, "png.deflate"]

        # self.root.ToBitmap().ToFile('Screenshot.bmp')
        # f = open(r'Screenshot.bmp', 'rb')
        # ls_f = base64.b64encode(f.read())
        # f.close()
        # return [ls_f, "bmp"]

    def Click(self, x, y):
        self.SetForeground()
        size = self.root.AXSize
        pos = self.root.AXPosition
        pyautogui.moveTo(pos[0] + size[0] * x, pos[1] + size[1] * y)
        pyautogui.click(pos[0] + size[0] * x, pos[1] + size[1] * y)
        return True

    def Swipe(self, x1, y1, x2, y2, duration):
        self.SetForeground()
        Left = self.root.AXPosition[0]
        Top = self.root.AXPosition[1]
        Width = self.root.AXSize[0]
        Height = self.root.AXSize[1]
        x1 = Left + Width * x1
        y1 = Top + Height * y1
        x2 = Left + Width * x2
        y2 = Top + Height * y2
        pyautogui.moveTo(x1, y1)
        pyautogui.dragTo(x2, y2, duration)
        return True

    def LongClick(self, x, y, duration):
        self.SetForeground()
        Left = self.root.AXPosition[0]
        Top = self.root.AXPosition[1]
        Width = self.root.AXSize[0]
        Height = self.root.AXSize[1]
        x = Left + Width * x
        y = Top + Height * y
        pyautogui.moveTo(x, y)
        pyautogui.dragTo(x, y, duration)
        return True

    def EnumWindows(self, selector):
        names = []
        if 'bundleid' in selector:
            self.app = OSXFunc.getAppRefByBundleId(selector['bundleid'])
            windows = self.app.windows()
            for i, w in enumerate(windows):
                names.append((w.AXTitle, i))
            return names

        if 'appname' in selector:
            self.app = OSXFunc.getAppRefByLocalizedName(selector['appname'])
            windows = self.app.windows()
            for i, w in enumerate(windows):
                names.append((w.AXTitle, i))
            return names

        if 'appname_re' in selector:  # 此方法由于MacOS API，问题较多
            apps = OSXFunc.getRunningApps()  # 获取当前运行的所有应用程序
            appset = set()  # 应用程序集合
            appnameset = set()  # 应用程序标题集合
            for t in apps:
                tempapp = OSXFunc.getAppRefByPid(t.processIdentifier())
                if str(tempapp) == str(atomac.AXClasses.NativeUIElement()):  # 通过trick判断应用程序是都否为空
                    continue
                attrs = tempapp.getAttributes()
                if 'AXTitle' in attrs:
                    tit = tempapp.AXTitle
                    if re.match(selector['appname_re'], tit):
                        appset.add(tempapp)
                        appnameset.add(tit)  # 这里有Bug，可能会获取到进程的不同副本，所以要通过名字去判断是否唯一

            if len(appnameset) is 0:
                raise InvalidSurfaceException(selector, "Can't find any applications by the given parameter")
            if len(appnameset) != 1:
                raise NonuniqueSurfaceException(selector)
            while len(names) is 0:  # 有可能有多个副本，但只有一个真的应用程序有窗口，所以要枚举去找
                if len(appset) is 0:
                    return names
                self.app = appset.pop()
                windows = self.app.windows()  # 获取当前应用程序的所有窗口
                for i, w in enumerate(windows):
                    names.append((w.AXTitle, i))
            return names
        return names
        
    def ConnectWindowsByWindowTitle(self, selector, wlist):
        hn = set()
        for n in wlist:
            if selector['windowtitle'] == n[0]:
                hn.add(n[1])
        if len(hn) == 0:
            return -1
        return hn

    def ConnectWindowsByWindowTitleRe(self, selector, wlist):
        hn = set()
        for n in wlist:
            if re.match(selector['windowtitle_re'], n[0]):
                hn.add(n[1])
        if len(hn) == 0:
            return -1
        return hn

    def ConnectWindow(self, selector):
        
        # 目前来说，如下处理，以后添加更多的参数后需修改代码逻辑
        argunums = 0
        if 'bundleid' in selector:
            argunums += 1
        if 'appname' in selector:
            argunums += 1
        if 'appname_re' in selector:
            argunums += 1
        if argunums == 0:
            raise ValueError("Expect bundleid or appname, got none")
        elif argunums != 1:
            raise ValueError("Too many arguments, only need bundleid or appname or appname_re")
        
        winlist = self.EnumWindows(selector)

        handleSetList = []
        if 'windowtitle' in selector:
            handleSetList.append(self.ConnectWindowsByWindowTitle(selector, winlist))
        if 'windowindex' in selector:
            handleSetList.append(set([selector['windowindex']]))
        if "windowtitle_re" in selector:
            handleSetList.append(self.ConnectWindowsByWindowTitleRe(selector, winlist))

        while -1 in handleSetList:
            handleSetList.remove(-1)

        if len(handleSetList) == 0:  # 三种方法都找不到窗口
            raise InvalidSurfaceException(selector, "Can't find any applications by the given parameter")
            
        handleSet = reduce(operator.__and__, handleSetList)

        if len(handleSet) == 0:
            raise InvalidSurfaceException(selector, "Can't find any applications by the given parameter")
        elif len(handleSet) != 1:
            raise NonuniqueSurfaceException(selector)
        else:
            hn = handleSet.pop()
            w = self.app.windows()
            if len(w) <= hn:
                raise IndexError("Unable to find the specified window through the index, you may have closed the specified window during the run")
            self.root = self.app.windows()[hn]
            self.SetForeground()

    def run(self):
        self.reactor = StdRpcReactor()
        self.reactor.register('Dump', self.Dump)
        self.reactor.register('GetSDKVersion', self.GetSDKVersion)
        self.reactor.register('GetDebugProfilingData', self.GetDebugProfilingData)
        self.reactor.register('GetScreenSize', self.GetScreenSize)
        self.reactor.register('Screenshot', self.Screenshot)
        self.reactor.register('Click', self.Click)
        self.reactor.register('Swipe', self.Swipe)
        self.reactor.register('LongClick', self.LongClick)
        self.reactor.register('SetForeground', self.SetForeground)
        self.reactor.register('ConnectWindow', self.ConnectWindow)
        transport = TcpSocket()
        transport.bind(self.addr)
        self.rpc = StdRpcEndpointController(transport, self.reactor)
        if self.running is False:
            self.running = True
            self.rpc.serve_forever()

if __name__ == '__main__':
    pocosdk = PocoSDKOSX()
    # pocosdk.ConnectWindow({'appname_re': u'系统偏好', 'windowindex': 0})
    # pocosdk.ConnectWindow({'appname': u'系统偏好设置', 'windowtitle': u'系统偏好设置'})
    # pocosdk.ConnectWindow({'bundleid': u'com.microsoft.VSCode', 'windowindex': 0})
    
    pocosdk.run()
