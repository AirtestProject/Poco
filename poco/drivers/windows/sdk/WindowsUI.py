# coding=utf-8

from poco.utils.net.stdrpc import RpcDispatcher
from WindowsUIDumper import WindowsUIDumper
from WindowsUINode import WindowsUINode
from poco.sdk.exceptions import UnableToSetAttributeException
from poco.utils.six import text_type
from uiautomation import uiautomation as UIAuto
import time
import json
import base64
import zlib
import win32api
import win32con
import win32gui
import re

DEFAULT_PORT = 15004
DEFAULT_ADDR = ('0.0.0.0', DEFAULT_PORT)

class PocoSDKWindows(object):
    
    def __init__(self, addr=DEFAULT_ADDR):
        self.dispatcher = RpcDispatcher(addr)
        
        self.running =False
        UIAuto.OPERATION_WAIT_TIME = 0.1 # make operation faster,see uiautomation
        self.root = None 
        
        
    def Dump(self, _):
        res = WindowsUIDumper(self.root).dumpHierarchy()
        return res

    def SetText(self, id, val2):
        control = UIAuto.ControlFromHandle(id)
        if not control or not isinstance(val2,basestring):
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

    def Screenshot(self, width):
        # self.root.ToBitmap().ToFile('Screenshot.bmp')
        # f=open(r'Screenshot.bmp', 'rb') #二进制方式打开图文件
        # data = zlib.compress(f.read())
        # ls_f=base64.b64encode(data) #读取文件内容，转换为base64编码
        # f.close()
        # return [ls_f, "bmp.deflate"]

        self.root.ToBitmap().ToFile('Screenshot.bmp')
        f=open(r'Screenshot.bmp', 'rb') #二进制方式打开图文件
        ls_f=base64.b64encode(f.read()) #读取文件内容，转换为base64编码
        f.close()
        return [ls_f, "bmp"]

    def Click(self, x, y):
        self.root.Click(x, y)
        return True

    def Swipe(self, x1, y1, x2, y2, duration):
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
        win32gui.ShowWindow(self.root.Handle,win32con.SW_SHOWNORMAL)
        UIAuto.Win32API.SetForegroundWindow(self.root.Handle)
        return True

    def ConnectWindowsByName(self, name=None, print_hierarchy=False):
        if name != None and name != '':
            hn = win32gui.FindWindow(None, name)
            if hn == 0:
                return False
            else:
                self.root = UIAuto.ControlFromHandle(hn)
        else:
           return False

        if print_hierarchy:
            UIAuto.EnumAndLogControl(self.root)
        return True
    
    def ConnectWindowsByNameRe(self, name_re=None, print_hierarchy=False):
        if name_re != None:
            hn = 0
            hWndList = []
            def foo(hwnd,mouse):
                if win32gui.IsWindow(hwnd):
                    hWndList.append(hwnd)
            win32gui.EnumWindows(foo, 0)
            for handle in hWndList:
                title = win32gui.GetWindowText(handle)
                if re.match(name_re, title.decode("gbk")):
                    self.root = UIAuto.ControlFromHandle(handle)
                    hn = handle
                    break
            if hn == 0:
                return False
        else:
           return False

        if print_hierarchy:
            UIAuto.EnumAndLogControl(self.root)
        return True
    
    def ConnectWindowsByHandle(self, handle=None, print_hierarchy=False):
        if handle != None:
            title = win32gui.GetWindowText(handle) 
            if title:
                self.root = UIAuto.ControlFromHandle(handle)
            else:
                return False       
        else:
           return False

        if print_hierarchy:
            UIAuto.EnumAndLogControl(self.root)
        return True
        

    def run(self):
        if self.running == False:
            self.running = True
            # print "Current Window :", self.root.Name
            self.dispatcher.register('Dump', self.Dump)
            self.dispatcher.register('SetText', self.SetText)
            self.dispatcher.register('GetSDKVersion', self.GetSDKVersion)
            self.dispatcher.register('GetDebugProfilingData', self.GetDebugProfilingData)
            self.dispatcher.register('GetScreenSize', self.GetScreenSize)
            self.dispatcher.register('Screenshot', self.Screenshot)
            self.dispatcher.register('Click', self.Click)
            self.dispatcher.register('Swipe', self.Swipe)
            self.dispatcher.register('LongClick', self.LongClick)
            self.dispatcher.register('KeyEvent', self.KeyEvent)
            self.dispatcher.register('SetForeground', self.SetForeground)
            self.dispatcher.register('ConnectWindowsByName', self.ConnectWindowsByName)
            self.dispatcher.register('ConnectWindowsByNameRe', self.ConnectWindowsByNameRe)
            self.dispatcher.register('ConnectWindowsByHandle', self.ConnectWindowsByHandle)
            self.dispatcher.serve_forever()


if __name__ == '__main__':
    pocosdk = PocoSDKWindows()
    pocosdk.run()

 