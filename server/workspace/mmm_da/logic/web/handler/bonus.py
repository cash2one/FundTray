#!/usr/bin/python2.7
# coding=utf-8
"""
Created on 2016-1-9

@author: Jay
"""

from utils.route import route
from utils.network.http import HttpRpcHandler
from utils.wapper.web import web_adaptor
from mmm_da.lib.web import id_token_login
from utils import error_code
from mmm_da.lib.bonus import BonusLogMgr
from mmm_da.lib.web import body_json_parser


@route(r'/get_bonus_logs', name='get_bonus_logs')
class GetBonusLogHandler(HttpRpcHandler):
    @web_adaptor(body_parser_fun= body_json_parser)
    @id_token_login
    def post(self, account, page_idx=1, **kwargs):
        return {"result": error_code.ERROR_SUCCESS,
                "bonus_logs": BonusLogMgr().get_bonus_logs(account.id, page_idx)}
