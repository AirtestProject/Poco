# -*- coding: utf-8 -*-
# @Author: gzliuxin
# @Email:  gzliuxin@corp.netease.com
# @Date:   2017-07-11 14:25:58


class RpcInterface(object):
    """Base Rpc Client"""
    def __init__(self):
        super(RpcInterface, self).__init__()

    def get_screen_size(self):
        """get screen size"""
        raise NotImplementedError

    def getattr(self, nodes, name):
        """get node attribute"""
        raise NotImplementedError

    def setattr(self, nodes, name, val):
        """set node attribute"""
        raise NotImplementedError

    def select(self, query, multiple=False):
        """select nodes by query"""
        raise NotImplementedError

    def evaluate(self, obj_proxy):
        """
        临时接口，排除bug后移除
        返回对象本身即可

        :param obj_proxy: 
        :return: 
        """
        return obj_proxy


class RpcRemoteException(Exception):
    pass


class RpcTimeoutException(Exception):
    pass
