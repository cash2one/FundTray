#!/usr/bin/python2.7
# coding=utf-8
"""
Created on 2016-1-14

@author: Jay
"""
from utils.route import route
from utils.network.http import HttpRpcHandler
from utils.wapper.web import web_adaptor
from mmm_da.lib.account.control import AccountMgr
from mmm_da.lib.account.model import SEALED, ACTIVED
from utils import error_code
from utils import logger
from mmm_da.lib.web import id_passwd_login, require_admin_check
from mmm_da.lib.active import ActiveMgr
from mmm_da.lib.web import body_json_parser
from mmm_da.lib.token import TokenMgr

@route(r'/gm_login', name='gm_login')
class GMLoginHandler(HttpRpcHandler):
    @web_adaptor(body_parser_fun=body_json_parser)
    @id_passwd_login()
    @require_admin_check
    def post(self, account, **kwargs):
        return {"result": error_code.ERROR_SUCCESS,
                "account_info": account.get_info_dic(),
                "access_token": TokenMgr().generate_access_token(account.id)}

@route(r'/view_account/(?P<id>\S+)/(?P<passwd>\S+)/(?P<view_uid>\S+)', name='view_account')
class ViewAccountHandler(HttpRpcHandler):
    """
    账号查看
    """
    @web_adaptor()
    @id_passwd_login(required_admin=True)
    def get(self, account, view_uid, **kwargs):
        if not view_uid:
            logger.info("view_account get ERROR_UID_NOT_EXIST, not view_account")
            self.set_status(error_code.ERROR_UID_NOT_EXIST, 'Parameter Error')
            return error_code.ERROR_UID_NOT_EXIST

        view_account = AccountMgr().get_data_by_id(str(view_uid))
        if not view_account:
            logger.info("view_account get ERROR_UID_NOT_EXIST, not view_account!!!, view_uid" % view_uid)
            self.set_status(error_code.ERROR_UID_NOT_EXIST, 'Parameter Error')
            return error_code.ERROR_UID_NOT_EXIST

        return view_account.get_info_dic()


@route(r'/active_account/(?P<id>\S+)/(?P<passwd>\S+)/(?P<active_id>\S+)', name='active')
class ActiveHandler(HttpRpcHandler):
    """
    激活
    """
    @web_adaptor()
    @id_passwd_login(required_admin=True)
    def get(self, account, active_id, **kwargs):
        if not ActiveMgr().active_account(account, active_id):
            self.set_status(error_code.ERROR_LOGIC, 'Parameter Error')
            return error_code.ERROR_LOGIC
        return error_code.ERROR_SUCCESS


@route(r'/seal_account/(?P<id>\S+)/(?P<passwd>\S+)/(?P<seal_id>\S+)', name='seal account')
class SealAccountHandler(HttpRpcHandler):
    """
    封号
    """
    @web_adaptor()
    @id_passwd_login(required_admin=True)
    def get(self, seal_id, **kwargs):
        seal_account = AccountMgr().get_data_by_id(str(seal_id))
        if not seal_account:
            logger.info("seal_account get ERROR_UID_NOT_EXIST, not seal_account!!!, seal_id" % seal_id)
            self.set_status(error_code.ERROR_UID_NOT_EXIST, 'Parameter Error')
            return error_code.ERROR_UID_NOT_EXIST
        seal_account.attr_stat = SEALED
        return seal_account.get_info_dic()


@route(r'/unseal_account/(?P<id>\S+)/(?P<passwd>\S+)/(?P<unseal_id>\S+)', name='unseal account')
class UnsealAccountHandler(HttpRpcHandler):
    """
    解除封号
    """
    @web_adaptor()
    @id_passwd_login(required_admin=True)
    def get(self, unseal_id, **kwargs):
        unseal_account = AccountMgr().get_data_by_id(str(unseal_id))
        if not unseal_account:
            logger.info("unseal_account get ERROR_UID_NOT_EXIST, not seal_account!!!, unseal_id" % unseal_id)
            self.set_status(error_code.ERROR_UID_NOT_EXIST, 'Parameter Error')
            return error_code.ERROR_UID_NOT_EXIST

        # 解除封号以后，该账号进入激活状态，不需要激活币
        unseal_account.attr_stat = ACTIVED
        return unseal_account.get_info_dic()


@route(r'/add_active_coin/(?P<id>\S+)/(?P<passwd>\S+)/(?P<adding_id>\S+)/(?P<adding_coin>\S+)', name='add active coin')
class AddActiveCoinHandler(HttpRpcHandler):
    """
    增加激活币
    """
    @web_adaptor()
    @id_passwd_login(required_admin=True)
    def get(self, account, adding_id, adding_coin, **kwargs):
        if not adding_id or not adding_coin:
            logger.info("add_active_coin ERROR_UID_NOT_EXIST!!! not enough params")
            self.set_status(error_code.ERROR_UID_NOT_EXIST, 'Parameter Error')
            return error_code.ERROR_UID_NOT_EXIST

        adding_account = AccountMgr().get_data_by_id(adding_id)
        if not adding_account:
            logger.info("add_active_coin ERROR_UID_NOT_EXIST, not adding id, adding id:%s" % (adding_id))
            self.set_status(error_code.ERROR_UID_NOT_EXIST, 'Parameter Error')
            return error_code.ERROR_UID_NOT_EXIST
        adding_account.attr_active_coin += int(adding_coin)
        return adding_account.get_info_dic()


@route(r'/add_match_coin/(?P<id>\S+)/(?P<passwd>\S+)/(?P<adding_id>\S+)/(?P<adding_coin>\S+)', name='add match coin')
class AddMatchCoinHandler(HttpRpcHandler):
    """
    增加排单币
    """
    @web_adaptor()
    @id_passwd_login(required_admin=True)
    def get(self, account, adding_id, adding_coin, **kwargs):
        if not adding_id or not adding_coin:
            logger.info("add_match_coin ERROR_UID_NOT_EXIST!!! not enough params")
            self.set_status(error_code.ERROR_UID_NOT_EXIST, 'Parameter Error')
            return error_code.ERROR_UID_NOT_EXIST

        adding_account = AccountMgr().get_data_by_id(adding_id)
        if not adding_account:
            logger.info("add_match_coin ERROR_LOGIC, not adding id, adding id:%s" % (adding_id))
            self.set_status(error_code.ERROR_LOGIC, 'Parameter Error')
            return error_code.ERROR_LOGIC
        adding_account.attr_match_coin += int(adding_coin)
        logger.info("add_match_coin SUCCESS,adding id:%s, adding_coin:%s cur_match_coin:%s"
                    % (adding_id, adding_coin, adding_account.attr_match_coin))
        return adding_account.get_info_dic()