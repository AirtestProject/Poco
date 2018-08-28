# coding=utf-8

import fnmatch
import atomac
import AppKit
from atomac import _a11y
import Quartz

pressID = [None, Quartz.kCGEventLeftMouseDown,
           Quartz.kCGEventRightMouseDown, Quartz.kCGEventOtherMouseDown]
releaseID = [None, Quartz.kCGEventLeftMouseUp,
             Quartz.kCGEventRightMouseUp, Quartz.kCGEventOtherMouseUp]


class OSXFunc(object):

    @classmethod
    def getRunningApps(cls):
        ws = AppKit.NSWorkspace.sharedWorkspace()
        apps = ws.runningApplications()
        return apps

    @classmethod
    def getAppRefByPid(cls, pid):
        return _a11y.getAppRefByPid(atomac.AXClasses.NativeUIElement, pid)

    @classmethod
    def getAppRefByBundleId(cls, bundleId):
        """
        Get the top level element for the application with the specified
        bundle ID, such as com.vmware.fusion.
        """
        ra = AppKit.NSRunningApplication
        # return value (apps) is always an array. if there is a match it will
        # have an item, otherwise it won't.
        apps = ra.runningApplicationsWithBundleIdentifier_(bundleId)
        if len(apps) == 0:
            raise ValueError(('Specified bundle ID not found in '
                            'running apps: %s' % bundleId))
        pid = apps[0].processIdentifier()
        return cls.getAppRefByPid(pid)   

    @classmethod
    def getAppRefByLocalizedName(cls, name):
        apps = cls.getRunningApps()
        for app in apps:
            if fnmatch.fnmatch(app.localizedName(), name):
                pid = app.processIdentifier()
                return cls.getAppRefByPid(pid)
        raise ValueError('Specified application not found in running apps.')

    @staticmethod
    def press(x, y, button=1):
        event = Quartz.CGEventCreateMouseEvent(None, pressID[button], (x, y), button - 1)
        Quartz.CGEventPost(Quartz.kCGHIDEventTap, event)

    @staticmethod
    def release(x, y, button=1):
        event = Quartz.CGEventCreateMouseEvent(None, releaseID[button], (x, y), button - 1)
        Quartz.CGEventPost(Quartz.kCGHIDEventTap, event)

    @staticmethod
    def click(x, y, button=1):
        theEvent = Quartz.CGEventCreateMouseEvent(None, pressID[button], (x, y), button - 1)
        Quartz.CGEventPost(Quartz.kCGHIDEventTap, theEvent)  
        Quartz.CGEventSetType(theEvent, Quartz.kCGEventLeftMouseUp)  
        Quartz.CGEventPost(Quartz.kCGHIDEventTap, theEvent)  

    @staticmethod
    def rclick(x, y, button=2):
        theEvent = Quartz.CGEventCreateMouseEvent(None, pressID[button], (x, y), button - 1)
        Quartz.CGEventPost(Quartz.kCGHIDEventTap, theEvent)  
        Quartz.CGEventSetType(theEvent, releaseID[button])  
        Quartz.CGEventPost(Quartz.kCGHIDEventTap, theEvent)  

    @staticmethod
    def doubleclick(x, y, button=1):
        theEvent = Quartz.CGEventCreateMouseEvent(None, pressID[button], (x, y), button - 1)
        Quartz.CGEventSetIntegerValueField(theEvent, Quartz.kCGMouseEventClickState, 2)  
        Quartz.CGEventPost(Quartz.kCGHIDEventTap, theEvent)  
        Quartz.CGEventSetType(theEvent, Quartz.kCGEventLeftMouseUp)  
        Quartz.CGEventPost(Quartz.kCGHIDEventTap, theEvent)  
        Quartz.CGEventSetType(theEvent, Quartz.kCGEventLeftMouseDown) 
        Quartz.CGEventPost(Quartz.kCGHIDEventTap, theEvent)
        Quartz.CGEventSetType(theEvent, Quartz.kCGEventLeftMouseUp)
        Quartz.CGEventPost(Quartz.kCGHIDEventTap, theEvent)

    @staticmethod
    def move(x, y):
        move = Quartz.CGEventCreateMouseEvent(None, Quartz.kCGEventMouseMoved, (x, y), 0)
        Quartz.CGEventPost(Quartz.kCGHIDEventTap, move)

    @staticmethod
    def drag(x, y):
        drag = Quartz.CGEventCreateMouseEvent(None, Quartz.kCGEventLeftMouseDragged, (x, y), 0)
        Quartz.CGEventPost(Quartz.kCGHIDEventTap, drag)

    @staticmethod
    def scroll(vertical=None, horizontal=None, depth=None):
        # Local submethod for generating Mac scroll events in one axis at a time
        def scroll_event(y_move=0, x_move=0, z_move=0, n=1):
            for _ in range(abs(n)):
                scrollWheelEvent = Quartz.CGEventCreateScrollWheelEvent(
                    None,  # No source
                    Quartz.kCGScrollEventUnitLine,  # Unit of measurement is lines
                    3,  # Number of wheels(dimensions)
                    y_move,
                    x_move,
                    z_move)
                Quartz.CGEventPost(Quartz.kCGHIDEventTap, scrollWheelEvent)

        # Execute vertical then horizontal then depth scrolling events
        if vertical is not None:
            vertical = int(vertical)
            if vertical == 0:   # Do nothing with 0 distance
                pass
            elif vertical > 0:  # Scroll up if positive
                scroll_event(y_move=1, n=vertical)
            else:  # Scroll down if negative
                scroll_event(y_move=-1, n=abs(vertical))
        if horizontal is not None:
            horizontal = int(horizontal)
            if horizontal == 0:  # Do nothing with 0 distance
                pass
            elif horizontal > 0:  # Scroll right if positive
                scroll_event(x_move=1, n=horizontal)
            else:  # Scroll left if negative
                scroll_event(x_move=-1, n=abs(horizontal))
        if depth is not None:
            depth = int(depth)
            if depth == 0:  # Do nothing with 0 distance
                pass
            elif vertical > 0:  # Scroll "out" if positive
                scroll_event(z_move=1, n=depth)
            else:  # Scroll "in" if negative
                scroll_event(z_move=-1, n=abs(depth))
