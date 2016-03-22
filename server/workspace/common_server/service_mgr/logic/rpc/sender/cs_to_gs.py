#!/usr/bin/python2.7
# coding=utf-8
"""
Created on 2015-4-28

@author: Jay
"""
from utils.network.http import TcpRpcClient
from utils.wapper.catch import except_adaptor
from service_mgr.logic.rpc import TCP_SIGN
import ujson

class GsRpcClient(TcpRpcClient):
    """
    连接gs的rpc client
    """
    def __init__(self, host, port):
        super(GsRpcClient, self).__init__(str(host), int(port))

    @except_adaptor()
    def clear_cache(self):
        params = {"sign": TCP_SIGN}
        return self.fetch_sync("clear_cache", ujson.dumps(params))