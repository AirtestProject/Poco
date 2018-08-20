# coding=utf-8

import fnmatch
import atomac
import AppKit
from atomac import _a11y


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
