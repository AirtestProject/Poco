# coding=utf-8

from poco.sdk.interfaces.command import CommandInterface

__author__ = 'lxn3032'


class HunterCommand(CommandInterface):
    def __init__(self, hunter):
        self.hunter = hunter

    def command(self, cmd, type=None):
        """
        通过hunter调用gm指令，可调用hunter指令库中定义的所有指令，也可以调用text类型的gm指令
        gm指令相关功能请参考safaia GM指令扩展模块

        :param script: 指令
        :param lang: 语言，默认text
        :param sleep_interval: 调用指令后的等待间隔时间
        :return: None
        """

        type = type or 'text'
        self.hunter.script(cmd, lang=type)
