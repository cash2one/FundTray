#!/usr/bin/python2.7
# coding=utf-8
"""
Created on 2016-1-29

@author: Jay
"""
from utils.route import route
from utils.network.http import HttpRpcHandler
from utils.wapper.web import web_adaptor
from utils import error_code
from utils import logger
from mmm_da.lib.web import id_token_login
from mmm_da.lib.web import body_json_parser
from mmm_da.lib.account.control import AccountMgr


@route(r'/active_coin_transfer', name='active_coin_transfer')
class ActiveCoinTransferHandler(HttpRpcHandler):
    @web_adaptor(body_parser_fun= body_json_parser)
    @id_token_login
    def post(self, account, tgt_id, tgt_coin, **kwargs):
        tgt_coin = int(tgt_coin)
        tgt_account = AccountMgr().get_data_by_id(tgt_id)
        if not tgt_account:
            logger.info("active_coin_transfer ERROR_LOGIC, tgt_id:%s not exist" % tgt_id)
            self.set_status(error_code.ERROR_UID_NOT_EXIST, 'Parameter Error')
            return {"result": error_code.ERROR_UID_NOT_EXIST}

        if account.attr_active_coin < tgt_coin:
            logger.info("active_coin_transfer ERROR_LOGIC, active_coin:%s lack for tgt_coin:%s" %
                        (tgt_account.attr_active_coin,
                         tgt_coin))
            self.set_status(error_code.ERROR_LOGIC, 'Parameter Error')
            return {"result": error_code.ERROR_LOGIC}

        # 转账
        account.attr_active_coin -= tgt_coin
        tgt_account.attr_active_coin += tgt_coin
        return {"result": error_code.ERROR_SUCCESS}


@route(r'/match_coin_transfer', name='match_coin_transfer')
class MatchCoinTransferHandler(HttpRpcHandler):
    @web_adaptor(body_parser_fun= body_json_parser)
    @id_token_login
    def post(self, account, tgt_id, tgt_coin,  **kwargs):
        tgt_coin = int(tgt_coin)
        tgt_account = AccountMgr().get_data_by_id(tgt_id)
        if not tgt_account:
            logger.info("match_coin_transfer ERROR_LOGIC, tgt_id:%s not exist" % tgt_id)
            self.set_status(error_code.ERROR_UID_NOT_EXIST, 'Parameter Error')
            return {"result": error_code.ERROR_UID_NOT_EXIST}

        if account.attr_match_coin < tgt_coin:
            logger.info("match_coin_transfer ERROR_LOGIC, match_coin:%s lack for tgt_coin:%s" %
                        (tgt_account.attr_match_coin,
                         tgt_coin))
            self.set_status(error_code.ERROR_LOGIC, 'Parameter Error')
            return {"result": error_code.ERROR_LOGIC}

        # 转账
        account.attr_match_coin -= tgt_coin
        tgt_account.attr_match_coin += tgt_coin
        return {"result": error_code.ERROR_SUCCESS}
