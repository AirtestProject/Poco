# coding=utf-8


import unittest
from poco.drivers.android.uiautomation import AndroidUiautomationPoco


class TestNeteaseSdkLogin(unittest.TestCase):
    def test_normal_login(self):
        poco = AndroidUiautomationPoco()
        poco(textMatches='^.*登录方式$').wait_for_appearance()
        poco(textMatches='^.*邮箱.*$').click([0.5, -3])
        poco(nameMatches='^.*:id/netease_mpay__login_urs$').click()
        poco(nameMatches='^.*:id/netease_mpay__login_urs$').set_text('adolli@163.com')
        poco(nameMatches='.*:id/netease_mpay__login_login').click()
        poco(nameMatches='.*:id/netease_mpay__login_password').click()
        poco(nameMatches='.*:id/netease_mpay__login_password').set_text('********')
        poco(nameMatches='.*:id/netease_mpay__login_login').click()


if __name__ == '__main__':
    unittest.main()
