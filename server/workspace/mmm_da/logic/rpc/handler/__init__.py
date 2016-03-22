#!/usr/bin/python2.7
# coding=utf-8
"""
Created on 2015-4-28

@author: Jay
"""
from utils.network.tcp import TcpRpcHandler
from utils.wapper.stackless import gevent_adaptor
from utils.wapper.tcp import tcp_recv_adaptor
from utils import logger
from utils.wapper.crypto import sm_sign_checker


class RpcHandler(TcpRpcHandler):
    """
    TcpRpc事件处理类
    """
    @gevent_adaptor()
    @tcp_recv_adaptor()
    @sm_sign_checker()
    def clear_cache(self):
        """
        清除缓存
        :return:
        """
        logger.info("RpcHandler::clear_cache!!!")
