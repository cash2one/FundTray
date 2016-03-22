#!/usr/bin/python2.7
# coding=utf-8
"""
Created on 2015-12-20

@author: Jay
"""
import random
from utils.route import route
from utils.network.http import HttpRpcHandler
from utils.wapper.web import web_adaptor
from utils import error_code
from mmm_da.lib.server_info import ServerInfoMgr
from mmm_da.lib.web import id_token_login, account_active_check


@route(r'/system_info', name='system_info')
class SystemInfoHandler(HttpRpcHandler):
    @web_adaptor()
    @id_token_login
    @account_active_check
    def get(self, account, **kwargs):
        return {"apply_req_count": ServerInfoMgr().attr_total_apply_cnt,
                "accept_req_count": ServerInfoMgr().attr_total_accept_cnt,
                "notice": ServerInfoMgr().attr_notice}

@route(r'/new_account_id', name='new_account_id')
class NewAccountIDHandler(HttpRpcHandler):
    @web_adaptor()
    def get(self, **kwargs):
        new_account_id = ServerInfoMgr().attr_min_account_id + 1
        ServerInfoMgr().attr_min_account_id = new_account_id
        return {"result": error_code.ERROR_SUCCESS, "new_account_id":new_account_id}