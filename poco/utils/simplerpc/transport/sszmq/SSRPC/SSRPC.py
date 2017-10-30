# -*- coding: utf-8 -*-
"""----------------------------------------------------------------------------
Author:
	fengfan
	fengfan@corp.netease.com
Date:
	2017/1/10
Description:
	Sunshine RPC Module
History:
	2017/1/10, create file.
----------------------------------------------------------------------------"""
import sys
import uuid

is_py2 = sys.version[0] == '2'
if is_py2:
	from Queue import Queue, Empty
else:
	from queue import Queue, Empty

import msgpack
import zmq
import threading
import time

CMD_CREATE_SERVER = 1
CMD_CREATE_CLIENT = 2
CMD_SERVER_QUIT = 3
CMD_GET_SERVER_NODE = 4
_pack = lambda dat: msgpack.packb(dat, use_bin_type=True)
_unpack = lambda dat: msgpack.unpackb(dat, encoding="utf-8")

_zmq_context = None
_zmq_poll = None
_zmq_cmd_sock = None

_cmd_thread = None
_socket_thread = None
_project = None
_err_handler = None


class SSRPC_ERR(object):
	CONNECT_FAILED = 1  # 连接失败

def _err_msg(code, msg):
	if _err_handler:
		_err_handler(code, msg)
	else:
		# import traceback
		# traceback.print_stack()
		print("SSRPC errno:%d msg:%s"%(code, msg))

def _hex_str(tstr):
	return ":".join(hex(x if isinstance(x, int) else ord(x))[2:] for x in tstr)

_cmd_queue = Queue()
def cmd_loop(cmd_q, cmd_sock):
	while True:
		cmd = cmd_q.get()
		if isinstance(cmd, int):  # 退出
			break
		cmd_sock.send(_pack(cmd[0]))

		msg = cmd_sock.recv()
		msg = _unpack(msg)
		if cmd[1]:
			cmd[1](msg)

	# break out here
	cmd_sock.close()

_HEARTBEAT_SEC = 5
_HEARTBEAT_DATA = b'_ss_inner_heartbeat'
hb_time = 0
_sock_list = {}

def socket_loop(poller):
	hb_time = time.time() + _HEARTBEAT_SEC
	while True:
		socks = dict(poller.poll(_HEARTBEAT_SEC/2*1000))

		for s in socks:
			handler = _sock_list.get(s)
			if not handler:
				print(s, "has no handler???")
				continue

			if handler.is_server:
				msgs = s.recv_multipart()  # 只有两段，[ router对client分配的id，数据 ]，目前不允许发多段数据
				handler._on_multi_data(msgs)
			else:
				msg = s.recv()
				handler._on_raw_data(msg)

		if hb_time < time.time():  # 发送心跳包
			hb_time = time.time() + _HEARTBEAT_SEC
			for handler in _sock_list.values():
				handler.send_heartbeat()


def socket_tick():
	poller = _zmq_poll
	socks = dict(poller.poll(_HEARTBEAT_SEC / 2))

	for s in socks:
		handler = _sock_list.get(s)
		if not handler:
			print(s, "has no handler???")
			continue

		if handler.is_server:
			msgs = s.recv_multipart()  # 只有两段，[ router对client分配的id，数据 ]，目前不允许发多段数据
			handler._on_multi_data(msgs)
		else:
			msg = s.recv()
			handler._on_raw_data(msg)

	global hb_time
	if hb_time < time.time():  # 发送心跳包
		hb_time = time.time() + _HEARTBEAT_SEC
		for handler in _sock_list.values():
			handler.send_heartbeat()


def cmd_tick():
	cmd_q = _cmd_queue
	cmd_sock = _zmq_cmd_sock
	try:
		cmd = cmd_q.get(False)
	except Empty:
		return
	if isinstance(cmd, int):  # 退出
		return

	cmd_sock.send(_pack(cmd[0]))

	msg = cmd_sock.recv()
	msg = _unpack(msg)
	if cmd[1]:
		cmd[1](msg)


_mode = 0
MAIN_THREAD_TICK = 0x1
MAIN_THREAD_SOCKET = 0x10
MAIN_THREAD_EVERYTHING = MAIN_THREAD_TICK | MAIN_THREAD_SOCKET
_callback_queue = Queue()


def init(projectID, mode=0, err_handler=None, addr="tcp://59.111.129.112:5560"):
	"""
	初始化SSRPC模块
	:param projectID: 你的项目代号，如G68
	:param mode: 启动模式，目前支持：
	MAIN_THREAD_TICK：由宿主来定时调用tick处理回调；否则将在socket线程自动回调；
	MAIN_THREAD_SOCKET: 由宿主来定时调用socket tick； 否则在子线程进行loop
	:param err_handler: 错误处理函数，格式：err_handler(code, msg)
	:param addr: broker地址，默认可不填写
	"""
	global _zmq_context
	global _zmq_poll
	global _zmq_cmd_sock
	global _cmd_thread
	global _socket_thread
	global _project
	global _mode
	global _err_handler

	assert projectID
	_project = projectID
	_mode = mode
	_err_handler = err_handler

	_zmq_context = zmq.Context()
	_zmq_cmd_sock = _zmq_context.socket(zmq.REQ)
	_zmq_cmd_sock.connect(addr)

	_zmq_poll = zmq.Poller()

	if not mode & MAIN_THREAD_SOCKET:
		_cmd_thread = threading.Thread(target=cmd_loop, args=(_cmd_queue, _zmq_cmd_sock))
		_cmd_thread.daemon = True
		_cmd_thread.start()
		_socket_thread = threading.Thread(target=socket_loop, args=(_zmq_poll,))
		_socket_thread.daemon = True
		# _socket_thread.start()

if not is_py2:
	def _convert_bytes_to_str(data):
		if isinstance(data, bytes):
			return data.decode()
		elif isinstance(data, (tuple, list)):
			return [_convert_bytes_to_str(x) for x in data]
		elif isinstance(data, dict):
			new_dict = {}
			for k, v in data.items():
				new_dict[_convert_bytes_to_str(k)] = _convert_bytes_to_str(v)
			return new_dict
		else:
			return data


def _send_cmd(data, cb=None):
	_cmd_queue.put([data, cb])


def _setup_cb(handler, new_addr):
	global _sock_list
	if not new_addr:
		_err_msg(SSRPC_ERR.CONNECT_FAILED, "try connect to %s failed" % handler._to_server_id)
		return
	new_sock = _zmq_context.socket(zmq.DEALER)
	new_sock.connect(new_addr)
	_zmq_poll.register(new_sock, zmq.POLLIN)
	if not(_mode & MAIN_THREAD_SOCKET) and (not _socket_thread.is_alive()):
		_socket_thread.start()
	_sock_list[new_sock] = handler
	# print(handler)
	handler.set_zmq_socket(new_sock)
	handler.on_init_finish(True)
	print("create", "server" if handler.is_server else "client", "done ->", new_addr)
	if not handler.is_server:
		try:
			import Atmosphere
			Atmosphere.EventParasiteConnected()
		except Exception as e:
			print(e)

SERV_MODE_ALL_GET_MSG = 0x1
def setup_server(server_ids, handler, mode=0):
	if not isinstance(server_ids, (tuple, list)):
		server_ids = [server_ids]
	data = {
		"server_ids": server_ids,
		"cmd": CMD_CREATE_SERVER,
		"proj": _project,
		"mode": mode,
	}

	handler._my_id = server_ids[0]
	_send_cmd(data, lambda msg: _setup_cb(handler, msg["rtn"]))


def setup_client(server_id, handler):
	handler._to_server_id = server_id
	import uuid
	handler._my_id = uuid.uuid4()
	data = {
		"server_id":server_id,
		"cmd":CMD_CREATE_CLIENT,
		"proj":_project,
	}
	_send_cmd(data, lambda msg: _setup_cb(handler, msg["rtn"]))


def get_server_node_info(project_id, callback):
	data = {
		"projectID": project_id,
		"cmd": CMD_GET_SERVER_NODE,
	}
	_send_cmd(data, lambda msg: callback(project_id, msg["rtn"]))


def _recv_node_cb(project_id, rtn):
	print("broker servers(project id: %s):" % project_id)
	for serv, ports in rtn.items():
		print("server id: %s, node ports: %s" % (serv, ports))


def tick():
	if _mode & MAIN_THREAD_TICK:
		while _callback_queue.qsize() > 0:
			cb = _callback_queue.get()
			cb[0]._exec_func(cb[1], cb[2])
	if _mode & MAIN_THREAD_SOCKET:
		socket_tick()
		cmd_tick()


def stop():
	pass
	# global _zmq_poll
	# global _sock_list

	# _cmd_thread.join()
	# _socket_thread.join()

	# _zmq_poll.close()
	# for sock, handler in _sock_list.items():
	# 	sock.close()
	# 	if handler.is_server:
	# 		_send_cmd(
	# 			{
	# 				"cmd":CMD_SERVER_QUIT,
	# 				"server_id":handler._my_id,
	# 				"proj":_project,
	# 			}
	# 		)
	# _sock_list = None

def ssrpc_method(rpcType=0):
	def _wrap_func(func):
		import sys
		classLocals = sys._getframe(1).f_locals
		dictName = "__rpc_methods__"
		if dictName not in classLocals:
			classLocals[dictName] = {"__ssrpc_callback__": lambda x: x}

		name = func.__name__

		assert name not in classLocals[dictName]
		classLocals[dictName][name] = rpcType
		return func
	return _wrap_func

def _ssrpc_class_inherit(clz):

	if not hasattr(clz, "__rpc_methods__") or "__inherited" in clz.__rpc_methods__:
		return
	rpc_dict = {"__inherited":True}
	for x in reversed(clz.mro()):
		if hasattr(x, "__rpc_methods__"):
			rpc_dict.update(x.__rpc_methods__)
	clz.__rpc_methods__ = rpc_dict


class _RPCb(object):
	'''
	SSRPC调用完后的返回对象，用于实现异步/同步(callback/wait)调用
	'''
	def __init__(self, prx):
		super(_RPCb, self).__init__()
		self.proxy = prx
		self.curr_sess_id = None

	def callback(self, func):
		assert self.curr_sess_id
		self.proxy.cb_list[self.curr_sess_id] = func
		self.curr_sess_id = None

	def wait(self, timeout=0):
		assert _mode & MAIN_THREAD_TICK, "wait can only be used in MAIN_THREAD_TICK mode"
		# TODO 加入Timeout
		old_time = (time.time() + timeout) if timeout > 0 else 0
		cache_cmd = []
		got_data = None
		while True:
			if _callback_queue.qsize() > 0:
				cb = _callback_queue.get()
				data = self.proxy.handler._unpack_data(cb[1])
				if data.get("__cb_session_id") == self.curr_sess_id:
					got_data = data
					break
				else:
					cache_cmd.append(cb)

			if old_time > 0 and time.time() > old_time:
				break

			time.sleep(0)

		for cmd in cache_cmd:  # 把cache的压回去
			_callback_queue.put(cmd)

		return got_data["__args"] if got_data else None


class _RPCProxy(object):
	'''
	具体的RPC调用对象，会把rpc封装成协议包发送，及解封接收到的包
	'''
	SUNSHINE_UUID = None

	def __init__(self, handler, is_server=False, reg_all=False):
		super(_RPCProxy, self).__init__()
		print (handler, is_server, reg_all);
		self.handler = handler
		self.is_server = is_server
		if reg_all:
			self.reg_all()
		if self.is_server:
			_ssrpc_class_inherit(self.__class__)
		self.cb_sess_id = None
		self.cb_sess_id_dict_for_server = {}
		self.cb_list = {}

		self.cb_obj = _RPCb(self)

	def __getitem__(self, client_id):
		self.client_id = client_id
		return self

	def __getattr__(self, item):
		def _call(*args, **kwargs):
			kwargs["__args"] = args
			kwargs["__rpc_func"] = item
			kwargs["__session_id"] = uuid.uuid4().hex
			kwargs["__handler_id"] = self.SUNSHINE_UUID
			if self.is_server:
				self.handler.send(self.client_id, kwargs)
				delattr(self, "client_id")
			else:
				self.handler.send(kwargs)

			self.cb_obj.curr_sess_id = kwargs["__session_id"]
			return self.cb_obj

		return _call

	def try_parse_kwargs(self, data):
		if isinstance(data, dict) and "__rpc_func" in data:
			func_name = data.pop("__rpc_func")

			if func_name in getattr(self.__class__, "__rpc_methods__", {}):
				func = getattr(self, func_name, None)
				args = data.pop("__args", [])
				return func, args, data, data.pop("__session_id", None), data.pop("__cb_session_id", None)
			else:
				raise RuntimeError("rpc function %s not found" % (func_name))

		return None, None, data, None, None

	def _exec_func(self, data, cid=None):
		# print("_exec_func", self, data)
		try:
			func, args, data, sid, cb_sid = self.try_parse_kwargs(data)
			if cb_sid:  # this is a callback message
				func = self.cb_list.pop(cb_sid, None)
				if func:
					func(*args, **data)
			elif func:
				# print("func:{}, args:{}, cid:{}, data:{}".format(func, args, cid, data))
				rtn = func(cid, *args, **data) if cid else func(*args, **data)

				if rtn is not None:  # callback message generate
					kwargs = {}
					kwargs["__rpc_func"] = "__ssrpc_callback__"
					kwargs["__args"] = [rtn] if not isinstance(rtn, tuple) else rtn
					kwargs["__cb_session_id"] = sid
					kwargs["__handler_id"] = self.SUNSHINE_UUID
					if self.is_server:
						self.handler.send(cid, kwargs)
					else:
						self.handler.send(kwargs)
			else:
				self.handler.on_data(cid, data) if cid else self.handler.on_data(data)
		except:
			import traceback
			traceback.print_exc()

	def reg_all(self):
		if not hasattr(self.__class__, "__rpc_methods__"):
			setattr(self.__class__, "__rpc_methods__", {})
		for k, func in self.Register(None).items():
			registry = self.__class__.__rpc_methods__
			registry[func.__name__] = func
			# print("reg", func)

	def Register(self, callServer):
		return {}


class ZMQHandler(object):
	_zmq_socket = None
	_my_id = None  # 这个并不是server.on_data里面的client_id
	_to_server_id = None

	def __init__(self):
		super(ZMQHandler, self).__init__()
		self._SSRPC = None
		self._rpc_registry = {}

	@property
	def is_server(self):
		return self._to_server_id is None

	@property
	def is_connected(self):
		return self._zmq_socket is not None

	def set_zmq_socket(self, so):
		self._zmq_socket = so
		self._zmq_cache_msgs = []
		if self.is_server:
			self.send(b"imsvr", self._my_id)

	def stop(self):
		self._zmq_socket = None

	_ZIP_MAGIC_STR = b"\xffsrz"  # zip的包头判定字符串
	_ZIP_MIN_SIZE = 1024  # 自动进行zip的包体大小下限

	def _unpack_data(self, data):
		if len(data) > 4 and data[:4] == self._ZIP_MAGIC_STR:
			import zlib
			data = zlib.decompress(data[4:])
		data = _unpack(data)

		if not is_py2:
			data = _convert_bytes_to_str(data)

		return data

	def _pack_data(self, data):
		data = _pack(data)
		if len(data) > self._ZIP_MIN_SIZE:
			import zlib
			data = self._ZIP_MAGIC_STR + zlib.compress(data)
		return data

	# @property
	# def SSRPC(self):
	# 	if not self._SSRPC:
	# 		self._SSRPC = _RPCProxy(self, self.is_server)
	# 	return self._SSRPC

	def register_rpc_handler(self, rpc_hanlder):
		if rpc_hanlder.SUNSHINE_UUID in self._rpc_registry:
			raise RuntimeError("duplicated SUNSHINE_UUID %s" % rpc_hanlder.SUNSHINE_UUID)
		self._rpc_registry[rpc_hanlder.SUNSHINE_UUID] = rpc_hanlder

	def _exec_func(self, data, cid=None):
		data = self._unpack_data(data)
		rpc_hanlder_id = data.pop("__handler_id")
		try:
			rpc_hanlder = self._rpc_registry[rpc_hanlder_id]
		except KeyError:
			print("SUNSHINE_UUID %s not found" % rpc_hanlder_id)
			return
		if _mode & MAIN_THREAD_TICK and threading.current_thread() is _socket_thread:
			_callback_queue.put([rpc_hanlder, data, cid])
		else:
			rpc_hanlder._exec_func(data, cid)
		# self.SSRPC._exec_func(data, cid)
	
	def __getitem__(self, handlerid):
		return self._rpc_registry[handlerid]


class SSRPCSvrHandler(ZMQHandler):
	def __init__(self):
		super(SSRPCSvrHandler, self).__init__()
		self.online_clients = {}
		self._clientInfoCBFunc = None

	def on_init_finish(self, rtn):
		pass

	def on_data(self, client_id, data):
		raise NotImplementedError()

	def on_client_connect(self, client_id):
		print("client", _hex_str(client_id), "connect")
		pass

	def on_client_disconnect(self, client_id):
		print("client", _hex_str(client_id), "disconnect")
		pass

	def _on_multi_data(self, msgs):
		self._zmq_cache_msgs.extend(msgs)
		while len(self._zmq_cache_msgs) >= 2:
			cid = self._zmq_cache_msgs.pop(0)
			data = self._zmq_cache_msgs.pop(0)
			if cid == b"myclients_cb":  # 特殊信息
				self.all_clients_info(_unpack(data))
				continue
			if cid not in self.online_clients:
				self.on_client_connect(cid)
			self.online_clients[cid] = time.time()

			if data != _HEARTBEAT_DATA:
				self._exec_func(data, cid)

	def send(self, client_id, data):
		self._zmq_socket.send_multipart([client_id, self._pack_data(data)])

	def return_sync_result(self, client_id, data, session_id):
		send_data = {"data": data, "__session_id": session_id}
		self._zmq_socket.send_multipart([client_id, self._pack_data(send_data)])

	def send_heartbeat(self):
		self._zmq_socket.send_multipart([_HEARTBEAT_DATA, _pack(self._my_id)])

		for cli in list(self.online_clients):
			if time.time() - self.online_clients[cli] > _HEARTBEAT_SEC * 2:
				self.online_clients.pop(cli)
				self.on_client_disconnect(cli)

	def get_all_clients(self, cbFunc=None):
		"""获取连接该节点的客户端信息，中心节点上的clients"""
		self.send(b"myclients", "")
		self._clientInfoCBFunc = cbFunc

	def all_clients_info(self, data):
		"""从连接节点返回的客户端信息"""
		if self._clientInfoCBFunc:
			self._clientInfoCBFunc(data)
		else:
			print("all connected clients:")
			for key, val in data.items():
				print("client: %s, info: %s" % (_hex_str(key), val))  # debug用


class SSRPCCliHandler(ZMQHandler):

	def __init__(self):
		self.__callbacks = {}  # callback缓存
		super(SSRPCCliHandler, self).__init__()

	def _registerCallback(self, callback):
		""" 注册回调 """
		callbackId = str(uuid.uuid4()).encode("UTF-8")  # python 2 与 3 的 str 不同，所以传bytes
		self.__callbacks[callbackId] = callback
		return callbackId

	@ssrpc_method()
	def callback(self, callback_id, *args, **kwargs):
		"""Server回调过来，根据 callback_id 找回 callback 函数"""
		callback_id = callback_id.encode("UTF-8")
		self.__callbacks[callback_id](*args, **kwargs)
		del self.__callbacks[callback_id]

	def on_init_finish(self, rtn):
		print("on_init_finish", self, rtn)

	def on_data(self, data):
		raise NotImplementedError()

	def _on_raw_data(self, data):
		self._exec_func(data)

	def send(self, data):
		if hasattr(self, "_zmq_socket") and self._zmq_socket is not None:
			self._zmq_socket.send(self._pack_data(data))

	def send_heartbeat(self):
		self._zmq_socket.send(_HEARTBEAT_DATA)
