# -*- coding: utf-8 -*-
"""----------------------------------------------------------------------------
Author:
	fengfan
	fengfan@corp.netease.com
Date:
	2017/1/10
Description:
	转发的中心节点
History:
	2017/1/10, create file.
----------------------------------------------------------------------------"""
import random
import threading
import time
import os
import sys
import zmq


BIND_IP = "0.0.0.0"  # 小小云不能bind外服ip，所以直接bind 0.0.0.0
IP = "59.111.129.112"  # 小小云外服IP
PORT = 5560

LOG_FILE = "./broker_connect.log"  # 现在日志都打在一起


# from .SSRPC import CMD_CREATE_SERVER, CMD_CREATE_CLIENT, CMD_SERVER_QUIT, _pack, _unpack, SERV_MODE_ALL_GET_MSG
CMD_CREATE_SERVER = 1
CMD_CREATE_CLIENT = 2
CMD_SERVER_QUIT = 3
CMD_GET_SERVER_NODE = 4

SERV_MODE_ALL_GET_MSG = 0x1
import msgpack
_pack = lambda dat: msgpack.packb(dat, use_bin_type=True)
_unpack = lambda dat: msgpack.unpackb(dat, encoding="utf-8")

def match_key(projectID, serverID):
	return (projectID, serverID)  # 用tuple存，为了查询用

_HEARTBEAT_SEC = 5
_HEARTBEAT_DATA = b'_ss_inner_heartbeat'
def new_pair(router_port, dealer_port, server_id, mode, log_file):
	import logging
	log = logging.getLogger(server_id)
	logFH = logging.FileHandler(log_file)
	logFH.setFormatter(logging.Formatter('%(asctime)s - %(filename)s - [line:%(lineno)d] - %(levelname)s - %(message)s'))
	log.addHandler(logFH)
	log.setLevel(logging.INFO)

	ctx = zmq.Context()
	client_router = ctx.socket(zmq.ROUTER)
	server_router = ctx.socket(zmq.ROUTER)
	client_router.bind("tcp://%s:%d"%(BIND_IP, router_port))
	server_router.bind("tcp://%s:%d"%(BIND_IP, dealer_port))

	log.info("pair process begin, router:%d <-> dealer:%d", router_port, dealer_port)

	server_ids = {}
	client_server_map = {}

	def hex_str(tstr):
		return ":".join(hex(x if isinstance(x, int) else ord(x))[2:] for x in tstr)

	def clear_client_server_map():
		now = time.time()
		for k in list(client_server_map):
			if now - client_server_map[k][1] > _HEARTBEAT_SEC*2:
				client_server_map.pop(k)
				log.info("client %s disconnect", hex_str(k))

	def clear_server_ids():
		now = time.time()
		for m in list(server_ids):
			if now - server_ids[m] > _HEARTBEAT_SEC*2:
				server_ids.pop(m)

	poller = zmq.Poller()
	poller.register(client_router, zmq.POLLIN)
	poller.register(server_router, zmq.POLLIN)
	while True:
		socks = dict(poller.poll(_HEARTBEAT_SEC/2*1000))

		if socks.get(client_router) == zmq.POLLIN:
			m = client_router.recv_multipart()
			# log.debug("client %s got message (%d) %s, %d"%(hex_str(m[0]), len(m), m[1], len(server_ids)))
			for i in range(0, len(m), 2):
				minfo = client_server_map.get(m[i])
				if not minfo:
					if len(server_ids) == 0: # TODO: 还没有server
						continue
					if mode & SERV_MODE_ALL_GET_MSG:
						minfo = ["\x0a\x11", 0]
					else:
						minfo = [random.choice(list(server_ids.keys())), 0]

					client_server_map[m[i]] = minfo
					log.info("client %s connect to %s", hex_str(m[i]), hex_str(minfo[0]))

				minfo[1] = time.time()
				# client heartbeat sends to server by f.f. 2017-02-22
				# if m[i+1] == _HEARTBEAT_DATA:
				# 	continue

				if minfo[0] is "\x0a\x11":  # all servers get msg, broadcast it
					for sid in server_ids:
						server_router.send_multipart([sid, m[i], m[i+1]])
					log.info("client:%s sends msg to all", hex_str(m[i]))
				else:
					server_router.send_multipart([minfo[0], m[i], m[i+1]])
					log.info("client:%s sends msg to %s", hex_str(m[i]), hex_str(minfo[0]))

		if socks.get(server_router) == zmq.POLLIN:
			m = server_router.recv_multipart()
			# log.debug("server %s got message (%d)"%(hex_str(m[0]), len(m)))
			for i in range(0, len(m), 3):
				# server send msg to me
				server_id = m[i]
				if m[i+1] == b"imsvr":  # reg server protocol
					server_ids[server_id] = time.time()
					log.info("server %s connect as %s", server_id, hex_str(m[i]))
					continue
				elif m[i+1] == _HEARTBEAT_DATA:  # server heart beat
					server_ids[server_id] = time.time()
					continue
				elif m[i+1] == b"myclients":  # get all clients in this node
					server_router.send_multipart([server_id, b"myclients_cb", _pack(client_server_map)])
					continue

				# server send msg to client
				client_router.send_multipart([m[i+1],m[i+2]])
				log.info("server:%s sends msg to %s", hex_str(m[i]), hex_str(m[i+1]))

		# 清理过期链接
		clear_client_server_map()
		old_server_cnt = len(server_ids)
		clear_server_ids()
		if old_server_cnt != 0 and len(server_ids) == 0:  # 可以下线了
			break

	client_router.close()
	server_router.close()
	ctx.term()
	log.info("pair process end, router:%d <-> dealer:%d", router_port, dealer_port)


def get_available_port_pair():
	import socket
	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	s.bind(("", 0))
	s.listen(1)
	sport = s.getsockname()[1]

	b = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	b.bind(("", 0))
	b.listen(1)
	bport = b.getsockname()[1]

	s.close()
	b.close()
	print("new pair socket create, router:%d <-> dealer:%d"%(sport, bport))
	return sport, bport

SERVER_INFO = {}
PROCESS_INFO = {}


def _send_msg(sock, data):
	sock.send(_pack(data))


def _check_sub_process_quit(sock_pairs, p):
	global SERVER_INFO
	global PROCESS_INFO
	p.join()
	PROCESS_INFO.pop(sock_pairs)
	for key in list(SERVER_INFO):
		if SERVER_INFO[key] == sock_pairs:
			SERVER_INFO.pop(key)
	print("socket_pair for %s terminated"%(str(sock_pairs)))


def on_create_server(sock, msg):
	# TODO: project info seperate
	global SERVER_INFO
	global PROCESS_INFO
	serv_ids = msg["server_ids"]

	for idt in serv_ids: # 检查一下是否已经有了对应的pair
		key = match_key(msg["proj"], idt)
		if key in SERVER_INFO:
			sock_pairs = SERVER_INFO[key]
			break # 有同名的
	else: # 没有
		sock_pairs = get_available_port_pair()
		from multiprocessing import Process
		p = Process(target=new_pair, args=list(sock_pairs)+[serv_ids[0], msg.get("mode", 0), LOG_FILE])
		p.daemon = True
		p.start()
		PROCESS_INFO[sock_pairs] = p
		threading.Thread(target=_check_sub_process_quit, name="%s_check"%(str(sock_pairs)), args=(sock_pairs, p)).start()
		print("%s: %s server set to pairs:%s, pid:%d"%(msg["proj"], serv_ids, sock_pairs, p.pid))

	for idt in serv_ids:
		key = match_key(msg["proj"], idt)
		if key in SERVER_INFO and SERVER_INFO[key] != sock_pairs:
			print("server:%s already has pairs:%s"%(key, SERVER_INFO[key]))
		SERVER_INFO[key] = sock_pairs

	msg[u"rtn"] = u"tcp://%s:%d"%(IP, sock_pairs[1])
	_send_msg(sock, msg)


def on_server_quit(sock, msg):
	global SERVER_INFO
	global PROCESS_INFO

	key = match_key(msg["proj"], msg["server_id"])
	pair = SERVER_INFO.get(key)
	if not pair:
		print("no such key: %s found"%(key))
		return

	finish_servers = []
	for k in SERVER_INFO.keys():
		if SERVER_INFO[k] == pair:
			SERVER_INFO.pop(k)
			finish_servers.append(k)

	p = PROCESS_INFO.get(pair)
	if p:
		print("process:%d terminate:%s"%(p.pid, pair))
		p.terminate()
	print("server:%s terminate"%(finish_servers))
	msg[u"rtn"] = 1
	_send_msg(sock, msg)


def on_create_client(sock, msg):
	key = match_key(msg["proj"], msg["server_id"])
	pair = SERVER_INFO.get(key)
	msg[u"rtn"] = 0 if not pair else (u"tcp://%s:%d" % (IP, pair[0]))
	_send_msg(sock, msg)


def get_connected_server_node(sock, msg):
	"""请求当前broker上所有与项目相关的连接，projectID为自己的项目号, 为空显示全部"""
	projectID = msg["projectID"]
	ret = {}
	for serv in SERVER_INFO:
		if serv[0] == projectID:
			ret[serv[1]] = SERVER_INFO[serv]
	msg[u"rtn"] = ret
	_send_msg(sock, msg)


CMD_DISPATCH = {
	CMD_CREATE_SERVER: on_create_server,
	CMD_SERVER_QUIT: on_server_quit,
	CMD_CREATE_CLIENT: on_create_client,
	CMD_GET_SERVER_NODE: get_connected_server_node,
}

def main():
	ctx = zmq.Context()
	cmd_dealer = ctx.socket(zmq.REP)
	try:
		cmd_dealer.bind("tcp://%s:%d"%(BIND_IP, PORT))
	except zmq.ZMQError as e:
		en = e.errno
		if en == zmq.EADDRINUSE:
			print("port:%d is in use"%PORT)
		else:
			print("bind error:%d"%en)
		exit(-1)

	while True:
		try:
			msg = cmd_dealer.recv()
		except KeyboardInterrupt:
			print("Keyboard Ctrl+C")
			break

		try:
			msg = _unpack(msg)
		except:
			print("message error:%s"%(msg))
			continue

		deal = CMD_DISPATCH.get(msg["cmd"])
		if not deal:
			print("wrong cmd:%s got"%(str(msg)))
		else:
			deal(cmd_dealer, msg)

	for _, sub_proc in PROCESS_INFO.items():
		sub_proc.join()
		sub_proc.terminate()

	print("Broker exit peacefully.")


if __name__ == "__main__":
	if len(sys.argv) > 1:
		LOG_FILE = sys.argv[1]  # 日志目录
	main()
