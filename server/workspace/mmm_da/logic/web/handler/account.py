#!/usr/bin/python2.7
# coding=utf-8
"""
Created on 2015-12-15

@author: Jay
"""
from utils.route import route
from utils.network.http import HttpRpcHandler
from utils.wapper.web import web_adaptor
from mmm_da.lib.token import TokenMgr
from mmm_da.lib.account.control import AccountMgr
from mmm_da.lib.account.model import MUST_KEY_SET, KEY_SET, SEALED
from mmm_da.lib.param import is_param_equal, is_param_in, get_valid_param
from utils import error_code
from utils import logger
from mmm_da.lib.web import body_json_parser
from mmm_da.lib.web import id_token_login, id_passwd_login
import random
from utils.regex import PHONE_REGEX
from mmm_da.lib.active import ActiveMgr


@route(r'/register', name='register')
class RegisterHandler(HttpRpcHandler):
    @web_adaptor(body_parser_fun= body_json_parser)
    def post(self, **kwargs):
        """
        data_dic:account, passwd,
        id_card, email, phone,
        leader_id,
        bank, bank_address, bank_account, bank_name,
        wechat, alipay
        :param kwargs:
        :return:
        """
        if not is_param_equal(kwargs, MUST_KEY_SET):
            logger.info("register ERROR_LOGIC, not is_param_equal, %s" % kwargs)
            self.set_status(error_code.ERROR_LOGIC, 'Parameter Error')
            return {"result": error_code.ERROR_LOGIC}

        if AccountMgr().is_id_exist(kwargs['id']):
            logger.info("register ERROR_LOGIC, id existed, %s" % kwargs['id'])
            self.set_status(error_code.ERROR_LOGIC, 'Parameter Error')
            return {"result": error_code.ERROR_LOGIC}

        valid_kwargs = get_valid_param(kwargs, KEY_SET)
        AccountMgr().create_account(valid_kwargs)
        return {"result": error_code.ERROR_SUCCESS}

@route(r'/login', name='login')
class LoginHandler(HttpRpcHandler):
    @web_adaptor(body_parser_fun=body_json_parser)
    @id_passwd_login()
    def post(self, account, **kwargs):
        return {"result": error_code.ERROR_SUCCESS,
                "account_info": account.get_info_dic(),
                "access_token": TokenMgr().generate_access_token(account.id)}


@route(r'/active/(?P<active_id>\S+)', name='logic_active')
class ActiveHandler(HttpRpcHandler):
    """
    激活
    """
    @web_adaptor()
    @id_token_login
    def post(self, account, active_id, **kwargs):
        if not ActiveMgr().active_account(account, active_id):
            self.set_status(error_code.ERROR_LOGIC, 'Parameter Error')
            return error_code.ERROR_LOGIC
        return error_code.ERROR_SUCCESS

@route(r'/account/(?P<do_id>\S+)', name='modify/get account infos')
class AccountHandler(HttpRpcHandler):
    @web_adaptor(body_parser_fun=body_json_parser)
    @id_token_login
    def post(self, account, **kwargs):
        if not is_param_in(kwargs, KEY_SET):
            logger.info("account post ERROR_LOGIC, not is_param_in, id:%s" % account.id)
            self.set_status(error_code.ERROR_LOGIC, 'Parameter Error')
            return {"result": error_code.ERROR_LOGIC}

        valid_kwargs = get_valid_param(kwargs, KEY_SET)
        account.update_data(valid_kwargs)
        return {"result": error_code.ERROR_SUCCESS}

    @web_adaptor()
    @id_token_login
    def get(self, account, do_id, **kwargs):
        if not do_id:
            logger.info("account get ERROR_LOGIC, not do_id")
            self.set_status(error_code.ERROR_LOGIC, 'Parameter Error')
            return {"result": error_code.ERROR_LOGIC}

        is_self = str(account.id) == str(do_id)

        view_account = account \
            if is_self \
            else AccountMgr().get_data_by_id(str(do_id))
        if not view_account:
            logger.info("account get ERROR_LOGIC, not view_account!!!, do_id:%s" % do_id)
            self.set_status(error_code.ERROR_LOGIC, 'Parameter Error')
            return {"result": error_code.ERROR_LOGIC}

        return {"result": error_code.ERROR_SUCCESS,
                "account_info": view_account.get_info_dic() if is_self else view_account.view_info_dic() }


@route(r'/passwd_change', name='change passwd')
class PasswdChangeHandler(HttpRpcHandler):
    @web_adaptor(body_parser_fun=body_json_parser)
    @id_token_login
    def post(self, account, old_passwd, new_passwd, **kwargs):
        if account.attr_passwd != old_passwd:
            logger.info("passwd_change ERROR_LOGIC, oldpasswd is wrong!!!, passwd:%s, old_passwd:%s" % (account.passwd, old_passwd))
            self.set_status(error_code.ERROR_LOGIC, 'Parameter Error')
            return {"result": error_code.ERROR_LOGIC}

        account.attr_passwd = new_passwd
        return {"result": error_code.ERROR_SUCCESS}


@route(r'/random_leader_id', name='random_leader_id')
class RandomLeaderIDHandler(HttpRpcHandler):
    @web_adaptor()
    def get(self, **kwargs):
        return {"result": error_code.ERROR_SUCCESS,
                "leader_id":random.choice(AccountMgr().get_all_ids())}

@route(r'/check_id', name='check_id')
class CheckIDHandler(HttpRpcHandler):
    @web_adaptor(body_parser_fun=body_json_parser)
    def get(self, id, **kwargs):
        if not AccountMgr().is_id_exist(int(id)):
            logger.info("check_id ERROR_LOGIC, id:%s not exist" % id)
            self.set_status(error_code.ERROR_UID_NOT_EXIST, 'Parameter Error')
            return
        return

@route(r'/check_phone', name='check_phone')
class CheckPhoneHandler(HttpRpcHandler):
    @web_adaptor(body_parser_fun=body_json_parser)
    def get(self, phone, **kwargs):
        if not PHONE_REGEX.match(str(phone)):
            logger.info("check_phone ERROR_PHONE_INVALID phone:%s is invalid" % phone)
            self.set_status(error_code.ERROR_PHONE_INVALID, 'Parameter Error')
            return

        if AccountMgr().is_phone_exist(int(phone)):
            logger.info("check_phone ERROR_PHONE_EXISTED phone:%s has existed" % phone)
            self.set_status(error_code.ERROR_PHONE_EXISTED, 'Parameter Error')
            return
        return

