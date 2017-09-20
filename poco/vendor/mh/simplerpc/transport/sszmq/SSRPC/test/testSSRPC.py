# -*- coding: utf-8 -*-
"""---------------------------------------------------------------------
Author:
guoxiaocan
gzguoxiaocan@corp.netease.com

Date:
2017/2/13

Description:

History:
2017/2/13, create file.
---------------------------------------------------------------------"""
import sys
sys.path.append("..")

import time
from SSRPC import MAIN_THREAD_TICK
from SSRPC import SERV_MODE_ALL_GET_MSG
from SSRPC import SSRPCCliHandler
from SSRPC import SSRPCSvrHandler
from SSRPC import init
from SSRPC import setup_client
from SSRPC import setup_server
from SSRPC import ssrpc_method
from SSRPC import tick


class SH(SSRPCSvrHandler):
	def on_init_finish(self, rtn):
		print(self._my_id, "init ok")

	def on_data(self, client_id, data):
		print(self._my_id, "server from", client_id, "on_data", data)
		self.send(client_id, "efg")

	@ssrpc_method()
	def foo(self, client_id, data):
		print(self._my_id, "server from", client_id, "rpc_func foo", data)
		self.SSRPC[client_id].bar("efg")

	@ssrpc_method()
	def foo2(self, client_id, data):
		print(self._my_id, "server from", client_id, "rpc_func foo", data)
		return "ijk", "lmn"


class CH(SSRPCCliHandler):
	def __init__(self):
		super(SSRPCCliHandler, self).__init__()
		self.count = 0

	def _callback(self, x, y):
		print("callback", x, y)
		self.my_send()

	def my_send(self):
		self.count += 1
		if self.count > 10:
			return
		elif self.count > 8:
			rtn = self.SSRPC.foo2({"ghi":self.count}).wait()
			print("sync call", rtn)
			self.my_send()
		elif self.count > 6:
			self.SSRPC.foo2({"def":self.count}).callback(self._callback)
		elif self.count > 3:
			self.SSRPC.foo({"def":self.count})
		else:
			self.send({"abc":self.count , "cdf":"abc"*1024})

	def on_init_finish(self, rtn):
		print(self._my_id, "SSRPCCliHandler init ok")
		self.my_send()

	def on_data(self, data):
		print(self._my_id, "client on_data", data)
		self.my_send()

	@ssrpc_method()
	def bar(self, test_str):
		print(self._my_id, "client rpc_func bar", test_str)
		self.my_send()

def my_err_handler(code, msg):
	print("my_err_handler %d %s"%(code, msg))

init("g68", MAIN_THREAD_TICK, my_err_handler)

def server_test():
	print("setup_server")
	setup_server("ff_server", SH(), SERV_MODE_ALL_GET_MSG)
	setup_server(["server1","ff_server"], SH(), SERV_MODE_ALL_GET_MSG)

	while True:
		tick()
		time.sleep(0.1)

from threading import Thread
p = Thread(target=server_test)
p.daemon = True
p.start()

time.sleep(1)

# setup_client("ff_server", CH())
# setup_client("ff_server", CH())
clientHandler = CH()
setup_client("ff_server", clientHandler)

import time
while True:
	tick()
	time.sleep(0.1)

