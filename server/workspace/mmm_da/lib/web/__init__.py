#!/usr/bin/python2.7
# coding=utf-8
"""
Created on 2015-12-15

@author: Jay
"""
import urllib2
import ujson
import time
from mmm_da.lib.account.control import AccountMgr, SYSTEM_ACCOUNT_ID
from mmm_da.lib.account.model import SEALED, UNACTIVED
from mmm_da.lib.token import TokenMgr
from utils import error_code, logger
from utils.service_control.parser import ArgumentParser


def body_json_parser(args, kwargs, body):
    """
    客户端请求的body网络适配器，
    :param args:
    :param kwargs:
    :param body:
    :return:
    """
    try:
        body = urllib2.unquote(body)
        body = ujson.loads(body)
        kwargs.update(body)
    except:
        logger.warn("body_json_parser failed!!! args:%s, kwargs:%s, body:%s"
                    %(args, kwargs, body))


def __is_account_valid(account,
                       enable_active=ArgumentParser().args.enable_active,
                       enable_seal=ArgumentParser().args.enable_seal):
    """
    判断账户是否有效
    :param account: 账户
    :param enable_active: 是否开启激活检测功能
    :param enable_seal:   是否开启封号检测功能
    :return:
    """
    if enable_seal and account.attr_stat == SEALED:
        logger.info("is_account_valid ERROR_LOGIC, account is sealed, id:%s" % account.id)
        return error_code.ERROR_ACCOUNT_SEALED

    if enable_active and account.attr_stat == UNACTIVED:
        logger.info("is_account_valid ERROR_LOGIC, account is unactived, id:%s" % account.id)
        return error_code.ERROR_ACCOUNT_UNACTIVED
    return error_code.ERROR_SUCCESS

def id_token_login(func):
    def wrapper(self, *args, **kwargs):
        headers = self.request.headers
        access_token = kwargs['access_token'] if "access_token" in kwargs else headers.get('Authorization', None)
        id = kwargs['id'] if "id" in kwargs else headers.get('id', None)

        if not id or not access_token:
            logger.info("%s: id_token_login ERROR_LOGIC!!! not id:%s or not access_token:%s" % (func, id, access_token))
            self.set_status(error_code.ERROR_LOGIC, 'Parameter Error')
            return {"result": error_code.ERROR_LOGIC}

        validate = TokenMgr().check_expire_access_token(access_token, id)
        if not validate:
            logger.info("%s: id_token_login ERROR_LOGIC!!! access_token not valid, id:%s access_token:%s" % (func, id, access_token))
            self.set_status(401, "Unauthorized(access token invalid)")
            return {"result": error_code.ERROR_LOGIC}

        from mmm_da.lib.account.control import AccountMgr
        account = AccountMgr().get_data_by_id(str(id))
        if not account:
            logger.info("%s: id_token_login ERROR_LOGIC!!! not account, id:%s" % (func, id))
            self.set_status(error_code.ERROR_LOGIC, 'Parameter Error')
            return {"result": error_code.ERROR_LOGIC}

        valid_result = __is_account_valid(account)
        if valid_result != error_code.ERROR_SUCCESS:
            logger.info("%s: is_account_valid %s!!! id:%s" % (func, valid_result, id))
            self.set_status(valid_result, 'Parameter Error')
            return {"result": valid_result}

        kwargs['account'] = account

        # 只要有访问服务器产生账号，就算登陆
        account.attr_login_time = time.time()
        return func(self, *args, **kwargs)
    return wrapper


def id_passwd_login(required_admin=False):
    def id_passwd_login_func_wrapper(func):
        def id_passwd_login_params_wrapper(self, id, passwd, *args, **kwargs):
            if not id or not passwd:
                logger.info("%s: id_passwd_login ERROR_LOGIC!!! not enough params" % func)
                self.set_status(error_code.ERROR_LOGIC, 'Parameter Error')
                return {"result": error_code.ERROR_LOGIC}

            if required_admin:
                if int(id) != int(SYSTEM_ACCOUNT_ID):
                    logger.info("%s: id_passwd_login ERROR_LOGIC!!! request system account" % func)
                    self.set_status(error_code.ERROR_LOGIC, 'Parameter Error')
                    return {"result": error_code.ERROR_LOGIC}

            account = AccountMgr().get_data_by_id(id)
            if not account or account.passwd != passwd:
                logger.info("%s:id_passwd_login ERROR_LOGIC, login error, id:%s, passwd:%s" % (func, id, passwd))
                self.set_status(error_code.ERROR_LOGIC, 'Parameter Error')
                return {"result": error_code.ERROR_LOGIC}

            valid_result = __is_account_valid(account)
            if valid_result != error_code.ERROR_SUCCESS:
                logger.info("%s: is_account_valid %s!!! id:%s" % (func, valid_result, id))
                self.set_status(valid_result, 'Parameter Error')
                return {"result": valid_result}

            kwargs['account'] = account

            # 只要有访问服务器产生账号，就算登陆
            account.attr_login_time = time.time()
            return func(self, *args, **kwargs)
        return id_passwd_login_params_wrapper
    return id_passwd_login_func_wrapper


def account_active_check(func):
    def wrapper(self, account, *args, **kwargs):
        valid_result = __is_account_valid(account)
        if valid_result != error_code.ERROR_SUCCESS:
            logger.info("%s: is_account_valid %s!!! id:%s" % (func, valid_result, id))
            self.set_status(valid_result, 'Parameter Error')
            return {"result": valid_result}

        return func(self, account, *args, **kwargs)
    return wrapper


def require_admin_check(func):
    def wrapper(self, account, *args, **kwargs):
        if int(account.id) != int(SYSTEM_ACCOUNT_ID):
            logger.info("%s: require_admin_check ERROR_LOGIC!!! request admin account" % func)
            self.set_status(error_code.ERROR_LOGIC, 'Parameter Error')
            return {"result": error_code.ERROR_LOGIC}
        return func(self, account, *args, **kwargs)
    return wrapper
