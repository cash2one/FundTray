#!/usr/bin/python2.7
# coding=utf-8
"""
Created on 2015-12-19

@author: Jay
"""
from utils.route import route
from utils.network.http import HttpRpcHandler
from utils.wapper.web import web_adaptor
from mmm_da.lib.web import id_token_login, account_active_check
from utils import error_code
from utils import logger
from mmm_da.lib.web import body_json_parser
from mmm_da.lib.help_req.control import ApplyHelpReqMgr, AcceptHelpReqMgr
from mmm_da.lib.help.control import ApplyHelpMgr, AcceptHelpMgr
from mmm_da.lib.help import accept_help_req_2_accept_help, apply_help_req_2_apply_help
from mmm_da.lib.help_pay.control import ApplyHelpPayMgr
from utils.comm_func import sub_dict
from mmm_da.lib.account.control import AccountMgr
from mmm_da.lib.server_info import ServerInfoMgr
from utils.service_control.parser import ArgumentParser


@route(r'/apply_help', name='apply_help')
class ApplyHelpHandler(HttpRpcHandler):
    @web_adaptor(body_parser_fun=body_json_parser)
    @id_token_login
    @account_active_check
    def post(self, account, apply_money, **kwargs):
        """
        申请帮助，同时只能有一个申请，且不论接受帮助的订单状态
        :param account: 账号
        :param apply_sorder_ls: 申请帮助完成订单
        :param kwargs:
        :return:
        """
        err_code = ApplyHelpReqMgr().do_req(account, apply_money)
        if err_code != error_code.ERROR_SUCCESS:
            self.set_status(err_code, 'Parameter Error')
            return

        apply_help_req = ApplyHelpReqMgr().get_unfinish(account.id)
        apply_help = apply_help_req_2_apply_help(apply_help_req)
        return {"result": error_code.ERROR_SUCCESS,
                "apply_help_ls": [apply_help] if apply_help else []}

@route(r'/del_apply_help',name='del_apply_help')
class DelApplyHelpHandler(HttpRpcHandler):
    @web_adaptor(body_parser_fun=body_json_parser)
    @id_token_login
    @account_active_check
    def post(self, account, apply_order, **kwargs):
        # 这里的apply_order是apply_help_req的id, 匹配以后就是apply_order父订单id
        apply_help_req = ApplyHelpReqMgr().get_unfinish(account.id)
        if not apply_help_req or apply_help_req['id'] != apply_order:
            logger.info("del_apply_help ERROR_LOGIC, not apply help req!!!, id:%s" % apply_order)
            self.set_status(error_code.ERROR_LOGIC, 'Parameter Error')
            return {"result": error_code.ERROR_LOGIC}

        ApplyHelpReqMgr().del_req(apply_order)
        logger.info("del_apply_help Success!!, uid:%s, apply_order:%s" % (account.id, apply_order))
        return {"result": error_code.ERROR_SUCCESS}


@route(r'/cur_apply_help', name='cur_apply_help')
class CurApplyHelpHandler(HttpRpcHandler):
    @web_adaptor()
    @id_token_login
    @account_active_check
    def post(self, account, **kwargs):
        apply_helps = ApplyHelpMgr().get_datas_by_uid(account.id)

        if not apply_helps:
            # 将申请帮助请求信息转化成申请帮助信息
            apply_help_req = ApplyHelpReqMgr().get_unfinish(account.id)
            apply_help = apply_help_req_2_apply_help(apply_help_req)
            logger.info("cur_apply_help Success!!, not apply_helps:%s, apply_help_req:%s" % (apply_helps, apply_help_req))
            return {"result": error_code.ERROR_SUCCESS,
                    "apply_help_ls": [],
                    "apply_help": apply_help}

        assert len(apply_helps) == 1
        cur_apply_help = apply_helps[0]
        cur_apply_help_pay_ls = ApplyHelpPayMgr().get_datas_by_apply_order(cur_apply_help['apply_order'])

        apply_help_ls = []
        for apply_help_pay_dic in cur_apply_help_pay_ls:
            # 获取申请帮助信息
            apply_res_dic = sub_dict(cur_apply_help, ['apply_order', 'apply_uid', 'apply_stime',])
            apply_res_dic.update(sub_dict(apply_help_pay_dic, ['apply_sorder', 'apply_pmoney', 'apply_mtime', 'apply_pstat', 'apply_piture', 'apply_message']))

            # 获取接受帮助信息
            accept_info = AcceptHelpMgr().get_data_by_order(apply_help_pay_dic['accept_order'])
            apply_res_dic['accept_uid'] = accept_info['accept_uid']

            # 获取接受帮助账号信息
            account_obj = AccountMgr().get_data_by_id(accept_info['accept_uid'])
            apply_res_dic['bank_name'] = account_obj.bank_name

            apply_help_ls.append(apply_res_dic)

        return {"result": error_code.ERROR_SUCCESS,
                "apply_help": cur_apply_help,
                "apply_help_ls": apply_help_ls}


@route(r'/apply_help_refuse', name='apply_help_refuse')
class ApplyHelpRefuseHandler(HttpRpcHandler):
    @web_adaptor(body_parser_fun=body_json_parser)
    @id_token_login
    @account_active_check
    def post(self, account, apply_sorder, **kwargs):
        # 获取申请帮助支付信息
        apply_help_pay = ApplyHelpPayMgr().get_data_by_sorder(apply_sorder)
        if not apply_help_pay:
            logger.info("apply_help_refuse ERROR_LOGIC, not apply_help!!!, apply_sorder:%s" % apply_sorder)
            self.set_status(error_code.ERROR_LOGIC, 'Parameter Error')
            return {"result": error_code.ERROR_LOGIC}

        # 获取申请帮助信息
        apply_help = ApplyHelpMgr().get_data_by_order(apply_help_pay['apply_order'])

        if apply_help['apply_uid'] != account.id:
            logger.info("apply_help_refuse ERROR_LOGIC, apply_sorder's apply uid not the account!!!, apply_uid:%s, id:%s" % (apply_help['apply_uid'], account.id))
            self.set_status(error_code.ERROR_LOGIC, 'Parameter Error')
            return {"result": error_code.ERROR_LOGIC}

        ApplyHelpMgr().do_deny_pay(apply_help_pay['apply_order'])
        ApplyHelpPayMgr().do_deny_pay(apply_sorder)
        return {"result": error_code.ERROR_SUCCESS}


@route(r'/accept_help', name='accept_help')
class AcceptHelpHandler(HttpRpcHandler):
    @web_adaptor(body_parser_fun=body_json_parser)
    @id_token_login
    @account_active_check
    def post(self, account, mafuluo, **kwargs):
        """
        接受帮助的时候，如果有一单申请帮助未完成，则不能接受帮助
        :param account: 账号
        :param mafuluo: 提取的马夫罗，整形
        :param kwargs:
        :return:
        """
        mafuluo = int(mafuluo)
        # 提取的马夫罗总数必须大于0
        if mafuluo <= 0 :
            logger.info("accept_help ERROR_LOGIC, mafuluo:%s<=0!!!, id:%s" % (mafuluo, account.id))
            self.set_status(error_code.ERROR_LOGIC, 'Parameter Error')
            return {"result": error_code.ERROR_LOGIC}

        # 提取的马夫罗必须小于账号拥有的马夫罗
        if mafuluo > account.attr_mafuluo:
            logger.info("accept_help ERROR_LOGIC, mafuluo:%s>=acount.attr_mafuluo:%s!!!, id:%s" % (mafuluo, account.attr_mafuluo, account.id))
            self.set_status(error_code.ERROR_LOGIC, 'Parameter Error')
            return {"result": error_code.ERROR_LOGIC}

        # 申请帮助还在请求处理，
        if ApplyHelpReqMgr().get_unfinish(account.id):
            logger.info("accept_help ERROR_LOGIC, has ApplyHelpReqMgr!!!, id:%s" % account.id)
            self.set_status(error_code.ERROR_LOGIC, 'Parameter Error')
            return {"result": error_code.ERROR_LOGIC}

        # 申请帮助还在匹配处理
        if ApplyHelpMgr().get_unfinish(account.id):
            logger.info("accept_help ERROR_LOGIC, has ApplyHelpMgr!!!, id:%s" % account.id)
            self.set_status(error_code.ERROR_LOGIC, 'Parameter Error')
            return {"result": error_code.ERROR_LOGIC}

        # 接受帮助还在请求处理，
        if AcceptHelpReqMgr().get_unfinish(account.id):
            logger.info("apply_help ERROR_LOGIC, has AcceptHelpReqMgr!!!, id:%s" % account.id)
            self.set_status(error_code.ERROR_LOGIC, 'Parameter Error')
            return {"result": error_code.ERROR_LOGIC}

        # 接受帮助还在匹配处理
        if AcceptHelpMgr().get_unfinish(account.id):
            logger.info("apply_help ERROR_LOGIC, has AcceptHelpMgr!!!, id:%s" % account.id)
            self.set_status(error_code.ERROR_LOGIC, 'Parameter Error')
            return {"result": error_code.ERROR_LOGIC}

        # 资金平衡判断
        if ArgumentParser().args.use_system_balance:
            if ServerInfoMgr().attr_total_accept_money + mafuluo + ServerInfoMgr().attr_system_balance\
                    > ServerInfoMgr().attr_total_apply_money:
                logger.info("accept_help ERROR_LOGIC, has reach the system balance!!!, "
                            "total_accept_money:%s, total_apply_money:%s, system_balance:%s, mafuluo:%s"
                            %(ServerInfoMgr().attr_total_accept_money,
                              ServerInfoMgr().attr_total_apply_money,
                              ServerInfoMgr().attr_system_balance,
                              mafuluo))
                self.set_status(error_code.EEROR_ACCEPT_BALANCE, 'Parameter Error')
                return

        # 扣除mafuluo
        account.attr_mafuluo -= mafuluo

        # 请求接受帮助
        AcceptHelpReqMgr().add_req(account.id, mafuluo)

        accept_help_req = AcceptHelpReqMgr().get_unfinish(account.id)
        return {"result": error_code.ERROR_SUCCESS,
                "accept_help": accept_help_req_2_accept_help(accept_help_req)}


@route(r'/del_accept_help',name='del_accept_help')
class DelAcceptHelpHandler(HttpRpcHandler):
    @web_adaptor(body_parser_fun=body_json_parser)
    @id_token_login
    @account_active_check
    def post(self, account, accept_order, **kwargs):
        # 这里的accept_order是accept_help_req的id, 匹配以后就是accept_order父订单id
        accept_help_req = AcceptHelpReqMgr().get_unfinish(account.id)
        if not accept_help_req or accept_help_req['id'] != accept_order:
            logger.info("del_accept_help ERROR_LOGIC, not accept help req!!!, id:%s" % accept_order)
            self.set_status(error_code.ERROR_LOGIC, 'Parameter Error')
            return {"result": error_code.ERROR_LOGIC}

        # 恢复对应马夫罗
        account.attr_mafuluo += accept_help_req['accept_req_money']

        # 删除请求队列
        AcceptHelpReqMgr().del_req(accept_order)

        logger.info("del_accept_help Success!!, uid:%s, accept_order:%s" % (account.id, accept_order))
        return {"result": error_code.ERROR_SUCCESS}


@route(r'/cur_accept_help', name='cur_accept_help')
class CurAcceptHelpHandler(HttpRpcHandler):
    @web_adaptor()
    @id_token_login
    @account_active_check
    def post(self, account, **kwargs):
        accept_help = AcceptHelpMgr().get_unfinish(account.id)

        if not accept_help:
            accept_help_req = AcceptHelpReqMgr().get_unfinish(account.id)
            return {"result": error_code.ERROR_SUCCESS,
                    "accept_help": accept_help_req_2_accept_help(accept_help_req),
                    "apply_help_ls": []}

        apply_help_ls =[]

        # 获取申请帮助子订单信息
        apply_help_pays = ApplyHelpPayMgr().get_datas_by_accept_order(accept_help['accept_order'])
        for apply_help_pay_dic in apply_help_pays:
            apply_help_dic = ApplyHelpMgr().get_data_by_order(apply_help_pay_dic['apply_order'])

            # 申请帮助信息
            apply_info = sub_dict(apply_help_dic, ['apply_order','apply_uid','apply_stime',])
            apply_info.update(sub_dict(apply_help_pay_dic, ['apply_sorder', 'apply_pmoney', 'apply_mtime', 'apply_pstat', 'apply_piture', 'apply_message']))

            # 申请帮助账号信息
            account_obj = AccountMgr().get_data_by_id(apply_help_dic['apply_uid'])
            apply_info['bank_name'] = account_obj.bank_name

            apply_help_ls.append(apply_info)
        return {"result": error_code.ERROR_SUCCESS,
                "accept_help": accept_help,
                "apply_help_ls": apply_help_ls}

@route(r'/accept_help_confirm', name='accept_help_confirm')
class AcceptHelpConfirmHandler(HttpRpcHandler):
    @web_adaptor(body_parser_fun=body_json_parser)
    @id_token_login
    @account_active_check
    def post(self, account, apply_sorder, **kwargs):
        # 获取申请帮助子订单信息
        apply_help_pay = ApplyHelpPayMgr().get_data_by_sorder(apply_sorder)
        if not apply_help_pay:
            logger.info("accept_help_confirm ERROR_LOGIC, not apply_help!!!, apply_sorder:%s" % apply_sorder)
            self.set_status(error_code.ERROR_LOGIC, 'Parameter Error')
            return {"result": error_code.ERROR_LOGIC}

        accept_order = apply_help_pay['accept_order']
        apply_order = apply_help_pay['apply_order']
        accept_help = AcceptHelpMgr().get_data_by_order(accept_order)

        if not accept_help:
            logger.info("accept_help_confirm ERROR_LOGIC, not accept_help!!!, accept_order:%s" % accept_order)
            self.set_status(error_code.ERROR_LOGIC, 'Parameter Error')
            return {"result": error_code.ERROR_LOGIC}

        if accept_help['accept_uid'] != account.id:
            logger.info("accept_help_confirm ERROR_LOGIC, apply_sorder's accept uid not the account!!!, uid:%s, account:%s" % (accept_help['accept_uid'], account.id))
            self.set_status(error_code.ERROR_LOGIC, 'Parameter Error')
            return {"result": error_code.ERROR_LOGIC}

        # 申请帮助支付订单确认
        ApplyHelpPayMgr().do_confirm(apply_sorder)

        # 申请帮助订单确认
        ApplyHelpMgr().do_confirm(apply_order)

        # 接受帮助订单确认
        AcceptHelpMgr().do_confirm(accept_order)
        return {"result": error_code.ERROR_SUCCESS}


@route(r'/accept_help_notreceived', name='accept_help_notreceived')
class AcceptHelpNotReceivedHandler(HttpRpcHandler):
    @web_adaptor(body_parser_fun=body_json_parser)
    @id_token_login
    @account_active_check
    def post(self, account, apply_sorder, **kwargs):
        # 获取申请帮助子订单信息
        apply_help_pay = ApplyHelpPayMgr().get_data_by_sorder(apply_sorder)
        if not apply_help_pay:
            logger.info("accept_help_confirm ERROR_LOGIC, not apply_help!!!, apply_sorder:%s" % apply_sorder)
            self.set_status(error_code.ERROR_LOGIC, 'Parameter Error')
            return {"result": error_code.ERROR_LOGIC}

        accept_order = apply_help_pay['accept_order']
        accept_help = AcceptHelpMgr().get_data_by_order(accept_order)

        if not accept_help:
            logger.info("accept_help_confirm ERROR_LOGIC, not accept_help!!!, accept_order:%s" % accept_order)
            self.set_status(error_code.ERROR_LOGIC, 'Parameter Error')
            return {"result": error_code.ERROR_LOGIC}

        if accept_help['accept_uid'] != account.id:
            logger.info("accept_help_confirm ERROR_LOGIC, apply_sorder's accept uid not the account!!!, uid:%s, account:%s" % (account.id, account))
            self.set_status(error_code.ERROR_LOGIC, 'Parameter Error')
            return {"result": error_code.ERROR_LOGIC}

        # 子订单完成
        ApplyHelpPayMgr().do_noreceived(apply_sorder)
        return {"result": error_code.ERROR_SUCCESS}