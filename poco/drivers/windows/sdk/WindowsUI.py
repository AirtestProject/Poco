# coding=utf-8

from poco.sdk.std.rpc.controller import StdRpcEndpointController
from poco.sdk.std.rpc.reactor import StdRpcReactor
from poco.utils.net.transport.tcp import TcpSocket
from poco.drivers.windows.sdk.WindowsUIDumper import WindowsUIDumper
from poco.sdk.exceptions import UnableToSetAttributeException, NonuniqueSurfaceException, InvalidSurfaceException
from poco.utils.six import string_types, PY2
import uiautomation as UIAuto
import time
import base64
import zlib
import win32con
import win32gui
import re

DEFAULT_PORT = 15004
DEFAULT_ADDR = ('0.0.0.0', DEFAULT_PORT)


class PocoSDKWindows(object):

    def __init__(self, addr=DEFAULT_ADDR):
        self.reactor = StdRpcReactor()
        self.reactor.register('Dump', self.Dump)
        self.reactor.register('SetText', self.SetText)
        self.reactor.register('GetSDKVersion', self.GetSDKVersion)
        self.reactor.register('GetDebugProfilingData', self.GetDebugProfilingData)
        self.reactor.register('GetScreenSize', self.GetScreenSize)
        self.reactor.register('Screenshot', self.Screenshot)
        self.reactor.register('Click', self.Click)
        self.reactor.register('Swipe', self.Swipe)
        self.reactor.register('LongClick', self.LongClick)
        self.reactor.register('KeyEvent', self.KeyEvent)
        self.reactor.register('SetForeground', self.SetForeground)
        self.reactor.register('ConnectWindow', self.ConnectWindow)

        transport = TcpSocket()
        transport.bind(addr)
        self.rpc = StdRpcEndpointController(transport, self.reactor)

        self.running = False
        UIAuto.OPERATION_WAIT_TIME = 0.1  # make operation faster
        self.root = None

    def Dump(self, _):
        res = WindowsUIDumper(self.root).dumpHierarchy()
        return res

    def SetText(self, id, val2):
        control = UIAuto.ControlFromHandle(id)
        if not control or not isinstance(val2, string_types):
            raise UnableToSetAttributeException("text", control)
        else:
            control.SetValue(val2)

    def GetSDKVersion(self):
        return '0.0.1'

    def GetDebugProfilingData(self):
        return {}

    def GetScreenSize(self):
        Width = self.root.BoundingRectangle[2] - self.root.BoundingRectangle[0]
        Height = self.root.BoundingRectangle[3] - self.root.BoundingRectangle[1]
        return [Width, Height]

    def JudgeSize(self):
        size = self.GetScreenSize()
        if size[0] == 0 or size[1] == 0:
            raise InvalidSurfaceException(self, "You may have minimized your window or the window is too small!")

    def Screenshot(self, width):
        self.JudgeSize()
        self.root.ToBitmap().ToFile('Screenshot.bmp')
        f = open(r'Screenshot.bmp', 'rb')
        deflated = zlib.compress(f.read())
        ls_f = base64.b64encode(deflated)
        f.close()
        return [ls_f, "bmp.deflate"]

        # self.root.ToBitmap().ToFile('Screenshot.bmp')
        # f = open(r'Screenshot.bmp', 'rb')
        # ls_f = base64.b64encode(f.read())
        # f.close()
        # return [ls_f, "bmp"]

    def Click(self, x, y):
        self.JudgeSize()
        self.root.Click(x, y)
        return True

    def Swipe(self, x1, y1, x2, y2, duration):
        self.JudgeSize()
        Left = self.root.BoundingRectangle[0]
        Top = self.root.BoundingRectangle[1]
        Width = self.root.BoundingRectangle[2] - self.root.BoundingRectangle[0]
        Height = self.root.BoundingRectangle[3] - self.root.BoundingRectangle[1]
        x1 = Left + Width * x1
        y1 = Top + Height * y1
        x2 = Left + Width * x2
        y2 = Top + Height * y2
        UIAuto.MAX_MOVE_SECOND = duration * 10
        UIAuto.DragDrop(int(x1), int(y1), int(x2), int(y2))
        return True

    def LongClick(self, x, y, duration):
        self.JudgeSize()
        Left = self.root.BoundingRectangle[0]
        Top = self.root.BoundingRectangle[1]
        Width = self.root.BoundingRectangle[2] - self.root.BoundingRectangle[0]
        Height = self.root.BoundingRectangle[3] - self.root.BoundingRectangle[1]
        x = Left + Width * x
        y = Top + Height * y
        UIAuto.MAX_MOVE_SECOND = duration * 10
        UIAuto.DragDrop(int(x), int(y), int(x), int(y))
        return True

    def KeyEvent(self, keycode):
        UIAuto.SendKeys(keycode)
        return True

    def SetForeground(self):
        win32gui.ShowWindow(self.root.Handle, win32con.SW_SHOWNORMAL)
        UIAuto.Win32API.SetForegroundWindow(self.root.Handle)
        return True

    def EnumWindows(self):
        hWndList = []

        def foo(hwnd, mouse):
            if win32gui.IsWindow(hwnd):
                hWndList.append(hwnd)
        win32gui.EnumWindows(foo, 0)
        return hWndList

    def ConnectWindowsByTitle(self, title):
        hn = set()
        hWndList = self.EnumWindows()
        for handle in hWndList:
            title_temp = win32gui.GetWindowText(handle)
            if PY2:
                title_temp = title_temp.decode("gbk")
            if title == title_temp:
                hn.add(handle)
        if len(hn) == 0:
            print
        return hn

    def ConnectWindowsByTitleRe(self, title_re):
        hn = set()
        hWndList = self.EnumWindows()
        for handle in hWndList:
            title = win32gui.GetWindowText(handle)
            if PY2:
                title = title.decode("gbk")
            if re.match(title_re, title):
                hn.add(handle)
        if len(hn) == 0:
            return -1
        return hn

    def ConnectWindowsByHandle(self, handle):
        hn = set()
        hWndList = self.EnumWindows()
        for handle_temp in hWndList:
            if int(handle_temp) == int(handle):
                hn.add(handle)
                break
        if len(hn) == 0:
            return -1
        return hn

    def ConnectWindow(self, selector, foreground=False):
        if foreground:
            time.sleep(1)
            self.root = UIAuto.GetForegroundControl()
            return True

        handleSetList = []
        if 'title' in selector:
            handleSetList.append(self.ConnectWindowsByTitle(selector['title']))
        if 'handle' in selector:
            handleSetList.append(self.ConnectWindowsByHandle(selector['handle']))
        if "title_re" in selector:
            handleSetList.append(self.ConnectWindowsByTitleRe(selector['title_re']))

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
            if hn:
                self.root = UIAuto.ControlFromHandle(hn)
                return True
            else:
                return False

    def run(self, use_foregrond_window=False):
        if self.running is False:
            self.running = True
            if use_foregrond_window:
                self.ConnectWindow(set(), True)
            self.rpc.serve_forever()

if __name__ == '__main__':
    pocosdk = PocoSDKWindows()
    pocosdk.run(True)
