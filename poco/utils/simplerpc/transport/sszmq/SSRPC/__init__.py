# -*- coding: utf-8 -*-
"""----------------------------------------------------------------------------
Author:
	fengfan
	fengfan@corp.netease.com
Date:
	2017/1/10
Description:
	SSRPC module, Base RPC Module used in Sunshine Project
History:
	2017/1/10, create file.
----------------------------------------------------------------------------"""

from .SSRPC import init, stop, setup_server, setup_client, ssrpc_method, tick
from .SSRPC import SSRPCSvrHandler, SSRPCCliHandler, ZMQHandler
from .SSRPC import _RPCProxy as RPCProxy
from .SSRPC import MAIN_THREAD_TICK, MAIN_THREAD_SOCKET, MAIN_THREAD_EVERYTHING, SSRPC_ERR, SERV_MODE_ALL_GET_MSG
