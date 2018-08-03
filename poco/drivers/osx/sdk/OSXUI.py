# coding=utf-8

import time
import base64
import zlib
import re
import pyautogui
import atomac
import AppKit
from poco.sdk.std.rpc.controller import StdRpcEndpointController
from poco.sdk.std.rpc.reactor import StdRpcReactor
from poco.utils.net.transport.tcp import TcpSocket
from poco.drivers.osx.sdk.OSXUIDumper import OSXUIDumper
from poco.sdk.exceptions import UnableToSetAttributeException, NonuniqueSurfaceException, InvalidSurfaceException
from poco.utils.six import string_types, PY2

DEFAULT_PORT = 15004
DEFAULT_ADDR = ('0.0.0.0', DEFAULT_PORT)


class PocoSDKOSX(object):

    def __init__(self, addr=DEFAULT_ADDR):
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
        transport.bind(addr)
        self.rpc = StdRpcEndpointController(transport, self.reactor)

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
            self.app = atomac.getAppRefByBundleId(selector['bundleid'])
            windows = self.app.windows()
            for i, w in enumerate(windows):
                names.append((w.AXTitle, i))
            return names

        if 'title' in selector:
            self.app = atomac.getAppRefByLocalizedName(selector['title'])
            windows = self.app.windows()
            for i, w in enumerate(windows):
                names.append((w.AXTitle, i))
            return names

        if 'title_re' in selector:
            apps = atomac.NativeUIElement._getRunningApps()

            s = set()
            sn = set()
            for t in apps:
                temp = atomac.getAppRefByPid(t.processIdentifier())
                if str(temp) == str(atomac.AXClasses.NativeUIElement()):
                    continue
                attrs = temp.getAttributes()
                if 'AXTitle' in attrs:
                    tit = temp.AXTitle
                    if re.match(selector['title_re'], tit):
                        s.add(temp)
                        sn.add(tit)  # 这里有Bug，可能会获取到相同的进程，所以要通过名字去判断是否唯一

            if len(sn) != 1:
                raise NonuniqueSurfaceException(selector)
            while len(names) is 0:
                if len(s) is 0:
                    return names
                self.app = s.pop()
                windows = self.app.windows()
                for i, w in enumerate(windows):
                    names.append((w.AXTitle, i))
            return names
        return names
        
    def ConnectWindowsByWindowName(self, selector, wlist):
        hn = set()
        for n in wlist:
            if selector['windowname'] == n[0]:
                hn.add(n[1])
        if len(hn) == 0:
            return -1
        return hn

    def ConnectWindowsByWindowNameRe(self, selector, wlist):
        hn = set()
        for n in wlist:
            if re.match(selector['windowname_re'], n[0]):
                hn.add(n[1])
        if len(hn) == 0:
            return -1
        return hn

    def ConnectWindow(self, selector):
        
        winlist = self.EnumWindows(selector)

        handleSetList = []
        if 'windowname' in selector:
            handleSetList.append(self.ConnectWindowsByWindowName(selector, winlist))
        if 'windownumber' in selector:
            handleSetList.append(set([selector['windownumber']]))
        if "windowname_re" in selector:
            handleSetList.append(self.ConnectWindowsByWindowNameRe(selector, winlist))

        while -1 in handleSetList:
            handleSetList.remove(-1)

        if len(handleSetList) == 0:
            return False

        handleSet = handleSetList[0]
        for s in handleSetList:
            handleSet = s & handleSet

        if len(handleSet) == 0:
            return False
        elif len(handleSet) != 1:
            raise NonuniqueSurfaceException(selector)
        else:
            hn = handleSet.pop()
            self.root = self.app.windows()[hn]
            
            self.SetForeground()
            return True

    def run(self):
        if self.running is False:
            self.running = True
            self.rpc.serve_forever()

if __name__ == '__main__':
    pocosdk = PocoSDKOSX()
    pocosdk.ConnectWindow({'title_re': u'系统偏好', 'windownumber': 0})
    pocosdk.run()
