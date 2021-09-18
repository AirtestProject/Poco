# coding=utf-8
__author__ = 'lnx3032'


import re

from airtest.utils.apkparser.apk import APK


def install(adb_client, localpath, force_reinstall=False):
    apk_info = APK(localpath)
    package_name = apk_info.package

    def _get_installed_apk_version(package):
        package_info = adb_client.shell(['dumpsys', 'package', package])
        matcher = re.search(r'versionCode=(\d+)', package_info)
        if matcher:
            return int(matcher.group(1))
        return None

    try:
        apk_version = int(apk_info.androidversion_code)
    except (RuntimeError, ValueError):
        apk_version = 0
    installed_version = _get_installed_apk_version(package_name)
    if installed_version is None or apk_version > installed_version or force_reinstall:
        print('installed version is {}, installer version is {}. force_reinstall={}'.format(installed_version,
                                                                                            apk_version,
                                                                                            force_reinstall))
        if installed_version is not None:
            force_reinstall = True
            uninstall(adb_client, package_name)
        if hasattr(adb_client, 'install_app'):
            adb_client.install_app(localpath, force_reinstall)
        else:
            adb_client.install(localpath, force_reinstall)
        return True
    return False


def uninstall(adb_client, package):
    if hasattr(adb_client, 'uninstall_app'):
        adb_client.uninstall_app(package)
    else:
        adb_client.uninstall(package)
