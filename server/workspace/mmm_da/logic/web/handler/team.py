#!/usr/bin/python2.7
# coding=utf-8
"""
Created on 2015-12-16

@author: Jay
"""

from utils.route import route
from utils.network.http import HttpRpcHandler
from utils.wapper.web import web_adaptor
from mmm_da.lib.web import id_token_login, account_active_check
from utils import error_code
from mmm_da.lib.team import TeamMgr


@route(r'/summary', name='summary')
class SummaryHandler(HttpRpcHandler):
    @web_adaptor()
    @id_token_login
    @account_active_check
    def post(self, account, **kwargs):
        return {"result": error_code.ERROR_SUCCESS, "summary": TeamMgr().summary(account.id)}
