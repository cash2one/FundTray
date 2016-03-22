#!/usr/bin/python2.7
# coding=utf-8
"""
Created on 2016-1-28

@author: Jay
"""
import time
from utils.route import route
from utils.network.http import HttpRpcHandler
from utils.wapper.web import web_adaptor
from utils import error_code
from utils import logger
from mmm_da.lib.server_info import ServerInfoMgr, CAN_UPDAET_KEY_SET
from mmm_da.lib.web import id_passwd_login, body_json_parser, id_token_login, require_admin_check
from mmm_da.lib.param import is_param_in, get_valid_param


@route(r'/all_server_setting', name='all server setting')
class AllServerSettingHandler(HttpRpcHandler):
    @web_adaptor()
    @id_token_login
    @require_admin_check
    def get(self, account, **kwargs):
        return ServerInfoMgr().get_info_dic()


@route(r'/reset_server_setting', name='reset server setting')
class ResetServerSettingHandler(HttpRpcHandler):
    @web_adaptor(body_parser_fun=body_json_parser)
    @id_token_login
    @require_admin_check
    def post(self, account, **kwargs):
        if not is_param_in(kwargs, CAN_UPDAET_KEY_SET):
            logger.info("account post ERROR_LOGIC, not is_param_in, id:%s" % account.id)
            self.set_status(error_code.ERROR_LOGIC, 'Parameter Error')
            return {"result": error_code.ERROR_LOGIC}

        valid_kwargs = get_valid_param(kwargs, CAN_UPDAET_KEY_SET)
        for k, v in valid_kwargs.items():
            ServerInfoMgr().update_value(k, v)
        return ServerInfoMgr().get_info_dic()


@route(r'/server_setting/(?P<id>\S+)/(?P<passwd>\S+)/(?P<field>\S+)/(?P<value>\S+)', name='server setting')
class ServerSettingHandler(HttpRpcHandler):
    @web_adaptor()
    @id_passwd_login(required_admin=True)
    def get(self, account, field, value, **kwargs):
        if field not in CAN_UPDAET_KEY_SET:
            self.set_status(error_code.ERROR_LOGIC, 'Parameter Error')
            return {"result": error_code.ERROR_LOGIC}

        ServerInfoMgr().update_value(field, value)
        return {"result": error_code.ERROR_SUCCESS,
                "server_info": ServerInfoMgr().get_info_dic()}


@route(r'/login_info/(?P<id>\S+)/(?P<passwd>\S+)/(?P<last_minutes>\S+)', name='login_info')
class LoginInfoHandler(HttpRpcHandler):
    @web_adaptor()
    @id_passwd_login(required_admin=True)
    def get(self, account, last_minutes, **kwargs):
        last_minutes = int(last_minutes)
        if last_minutes <= 0:
            return

        login_since_time = time.time() - last_minutes * 60

        sql = "SELECT COUNT(*) AS count  FROM ( SELECT id FROM account WHERE login_time >= %s GROUP BY id ) AS id_ls" \
              % int(login_since_time)

        logger.warn("login_info sql:%s" % sql)

        from mmm_da.db import DBAccountInst
        result = DBAccountInst.query(sql)
        return result[0]['count'] if result else result
