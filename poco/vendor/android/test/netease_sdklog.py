# coding=utf-8


import unittest
from poco.vendor.android.uiautomation import AndroidUiautomationPoco


class TestNeteaseSdkLogin(unittest.TestCase):
    def test_normal_login(self):
        poco = AndroidUiautomationPoco()
        poco(textMatches='^.*登录方式$').wait_for_appearance()
        poco(textMatches='^.*邮箱.*$').click([0.5, -3])
        poco('com.netease.my:id/netease_mpay__login_urs').click()
        poco('com.netease.my:id/netease_mpay__login_urs').set_text('adolli@163.com')
        poco('com.netease.my:id/netease_mpay__login_login').click()
        poco('com.netease.my:id/netease_mpay__login_password').click()
        poco('com.netease.my:id/netease_mpay__login_password').set_text('********')
        poco('com.netease.my:id/netease_mpay__password_login').click()


if __name__ == '__main__':
    unittest.main()
