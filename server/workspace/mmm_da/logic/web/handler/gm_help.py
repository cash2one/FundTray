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
from utils import error_code
from mmm_da.lib.web import id_token_login, account_active_check, id_passwd_login, require_admin_check
from mmm_da.lib.help_req.control import ApplyHelpReqMgr, AcceptHelpReqMgr
from mmm_da.lib.help.control import AcceptHelpMgr, ApplyHelpMgr
from mmm_da.lib.match import AcceptApplyMatcher
from utils import logger


@route(r'/add_accept_help/(?P<id>\S+)/(?P<passwd>\S+)/(?P<req_id>\S+)/(?P<req_money>\S+)', name='add_accept_help')
class AddAcceptHelpHandler(HttpRpcHandler):
    """
    增加接受帮助：跳过申请帮助阶段
    """
    @web_adaptor()
    @id_passwd_login(required_admin=True)
    def get(self, account, req_id, req_money, **kwargs):
        if not AccountMgr().is_id_exist(req_id):
            logger.info("AddAcceptHelpHandler ERROR_UID_NOT_EXIST, id not existed, %s" % req_id)
            self.set_status(error_code.ERROR_UID_NOT_EXIST, 'Parameter Error')
            return error_code.ERROR_UID_NOT_EXIST

        req_money = int(req_money)
        req_id = str(req_id)
        AcceptHelpReqMgr().add_req(req_id, req_money)
        accept_help_req = AcceptHelpReqMgr().get_unfinish(req_id)
        assert accept_help_req
        AcceptHelpReqMgr().do_match(accept_help_req['id'])
        return error_code.ERROR_SUCCESS


@route(r'/add_apply_help/(?P<id>\S+)/(?P<passwd>\S+)/(?P<req_id>\S+)/(?P<req_money>\S+)', name='add_apply_help')
class AddApplyHelpHandler(HttpRpcHandler):
    """
    增加申请帮助帮助：跳过申请帮助阶段
    """
    @web_adaptor()
    @id_passwd_login(required_admin=True)
    def get(self, account, req_id, req_money, **kwargs):
        if not AccountMgr().is_id_exist(req_id):
            logger.info("AddApplyHelpHandler ERROR_UID_NOT_EXIST, id not existed, %s" % req_id)
            self.set_status(error_code.ERROR_UID_NOT_EXIST, 'Parameter Error')
            return error_code.ERROR_UID_NOT_EXIST

        req_money = int(req_money)
        req_id = str(req_id)
        ApplyHelpReqMgr().add_req(req_id, req_money)
        apply_help_req = ApplyHelpReqMgr().get_unfinish(req_id)
        assert apply_help_req
        ApplyHelpReqMgr().do_match(apply_help_req['id'])
        return error_code.ERROR_SUCCESS

@route(r'/auto_match/(?P<id>\S+)/(?P<passwd>\S+)/(?P<apply_uid>\S+)/(?P<accept_uid>\S+)/(?P<apply_money>\S+)', name='auto_match')
class AutoMatchHandler(HttpRpcHandler):
    """
    自动匹配
    """
    @web_adaptor()
    @id_passwd_login(required_admin=True)
    def get(self, account, apply_uid, accept_uid, apply_money, **kwargs):
        apply_money = int(apply_money)

        if not AccountMgr().is_id_exist(apply_uid):
            logger.info("AutoMatchHandler ERROR_UID_NOT_EXIST, apply_uid not existed, %s" % apply_uid)
            self.set_status(error_code.ERROR_UID_NOT_EXIST, 'Parameter Error')
            return error_code.ERROR_UID_NOT_EXIST

        if not AccountMgr().is_id_exist(accept_uid):
            logger.info("AutoMatchHandler ERROR_UID_NOT_EXIST, id not existed, %s" % accept_uid)
            self.set_status(error_code.ERROR_UID_NOT_EXIST, 'Parameter Error')
            return error_code.ERROR_UID_NOT_EXIST

        # 获取申请帮助信息
        apply_help_dic = ApplyHelpMgr().get_unfinish(apply_uid)
        if not apply_help_dic:
            # 判断是否有申请帮助请求在排队，如果有，直接进入匹配模式
            apply_help_req = ApplyHelpReqMgr().get_unfinish(apply_uid)
            if not apply_help_req:
                logger.info("AutoMatchHandler ERROR_LOGIC, not apply_help_dic, apply_uid:%s" % apply_uid)
                self.set_status(error_code.ERROR_LOGIC, 'Parameter Error')
                return error_code.ERROR_LOGIC

            ApplyHelpReqMgr().do_match(apply_help_req['id'])
            apply_help_dic = ApplyHelpMgr().get_unfinish(apply_uid)
            assert apply_help_dic

        # 获取接受帮助信息
        accept_help_dic = AcceptHelpMgr().get_unfinish(accept_uid)
        if not accept_help_dic:
            accept_help_req = AcceptHelpReqMgr().get_unfinish(accept_uid)
            if not accept_help_req:
                logger.info("AutoMatchHandler ERROR_LOGIC, not accept_help_dic, accept_uid:%s" % accept_uid)
                self.set_status(error_code.ERROR_LOGIC, 'Parameter Error')
                return error_code.ERROR_LOGIC

            AcceptHelpReqMgr().do_match(accept_help_req['id'])
            accept_help_dic = AcceptHelpMgr().get_unfinish(accept_uid)
            assert accept_help_dic

        # 接受帮助金额判定
        apply_money = min(apply_money, apply_help_dic['apply_lmoney'], accept_help_dic['accept_lmoney'])

        # 手动匹配
        accept_matched_ls = [{"accept_order": accept_help_dic['accept_order'], "apply_money": apply_money}]
        AcceptApplyMatcher().matched_proc(apply_help_dic, accept_matched_ls)
        return error_code.ERROR_SUCCESS


@route(r'/apply_help_list', name='apply_help_list')
class ApplyHelpListHandler(HttpRpcHandler):
    @web_adaptor()
    @id_token_login
    @account_active_check
    @require_admin_check
    def post(self, account, **kwargs):
        return {"result": error_code.ERROR_SUCCESS,
                "apply_help_list": ApplyHelpMgr().match_ls()}


@route(r'/accept_help_list', name='accept_help_list')
class AcceptHelpListHandler(HttpRpcHandler):
    @web_adaptor()
    @id_token_login
    @account_active_check
    @require_admin_check
    def post(self, account, **kwargs):
        return {"result": error_code.ERROR_SUCCESS,
                "accept_help_list": AcceptHelpMgr().all_match_ls()}


