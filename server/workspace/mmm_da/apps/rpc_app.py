# coding=utf-8
"""
Created on 2015-4-25

@author: Jay
"""

from utils.meta.singleton import Singleton
from utils.network.tcp import TcpRpcServer
from mmm_da.logic.rpc import handler


class RpcApp(TcpRpcServer):
    """
    TcpRpc服务
    """
    __metaclass__ = Singleton

    def __init__(self, port,):
        # register handlers
        super(RpcApp, self).__init__(port, handler.RpcHandler)
