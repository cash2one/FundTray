#!/usr/bin/python2.7
# coding=utf-8
"""
Created on 2015-7-25

@author: Jay
"""
from gevent import monkey
monkey.patch_all()
import gsocketpool.pool
from mprpc import RPCPoolClient
from gevent.server import StreamServer
from mprpc import RPCServer
from utils.wapper.stackless import gevent_adaptor
from utils import logger
from utils.service_control.setting import PT_TCP
from utils.network import PING_RESPONSE


class TcpRpcHandler(RPCServer):
    """
    TcpRpc回调处理类
    """
    def ping(self):
        return PING_RESPONSE


class TcpRpcServer(object):
    """
    TcpRpc服务
    """
    def __init__(self, port, tcp_handler):
        self.port, self.class_type = port, tcp_handler
        self.server = StreamServer(('', self.port), self.class_type)
        self.protocol = PT_TCP

    @gevent_adaptor(use_join_result=False)
    def start(self):
        """
        服务开启
        :return:
        """
        logger.warn("start listen on %s:%s" % (self.protocol, self.port))
        self.server.serve_forever()

    def stop(self):
        """
        服务关闭
        :return:
        """
        self.server.stop()


class TcpRpcClient(object):
    """
    TcpRpc客户端
    """
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.client_pool = gsocketpool.pool.Pool(RPCPoolClient, dict(host=host, port=port), max_connections=2000)

    def __del__(self):
        # 程序退出的时候没有自动调用client_poll,没有stop所有的连接，所以手动调用一下
        if "client_pool" in self.__dict__:
            self.client_pool.__del__()

    def _rpc_fetch(self, func_name, *args):
        """
        rpc函数调用实现
        :param func_name:函数名
        :param args: 参数
        :return:函数调用结果
        """
        with self.client_pool.connection() as client:
            try:
                result = client.call(func_name, *args)
            except:
                logger.warn("TcpRpcClient::_rpc_fetch recall!!!, host:%s, port:%s, func_name:%s args:%s" %
                            (self.host,
                             self.port,
                             func_name,
                             args))
                # if reconnect, recall again
                result = client.call(func_name, *args)
            return result

    @gevent_adaptor()
    def fetch_async(self, func_name, *args):
        """
        协程非阻塞调用
        :param func_name:
        :param args:
        :return:
        """
        return self._rpc_fetch(func_name, *args)

    def fetch_sync(self, func_name, *args):
        """
        阻塞调用
        :param func_name:
        :param args:
        :return:
        """
        return self._rpc_fetch(func_name, *args)

    def ping(self):
        """
        ping 函数调用
        :return:
        """
        return self.fetch_sync("ping")

    def open(self):
        """
        打开连接，不处理，checker使用的时候兼容系统类
        :return:
        """
        return self

    def is_expired(self):
        """
        判断是否过期，不处理，checker使用的时候兼容系统类
        :return:
        """
        return False