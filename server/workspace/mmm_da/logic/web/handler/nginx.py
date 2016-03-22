#!/usr/bin/python2.7
# coding=utf-8
"""
Created on 2015-12-25

@author: Jay
"""
import os
from utils.route import route
from utils.network.http import HttpRpcHandler
from utils.wapper.web import web_adaptor
from mmm_da.lib.web import id_token_login, account_active_check
from mmm_da.lib.help_pay.control import ApplyHelpPayMgr
from mmm_da.lib.help.control import ApplyHelpMgr
from utils import logger, error_code
import time
from utils.service_control.parser import ArgumentParser
import urllib2
from mmm_da.lib.nginx import mv_pay_pic
from mmm_da.lib.help_pay.setting import APYS_PAY_WAIT


@route(r'/apply_help_paid', name='apply_help_paid')
class ApplyHelpPaidHandler(HttpRpcHandler):
    @web_adaptor()
    @id_token_login
    @account_active_check
    def post(self, account, apply_sorder, pay_msg="", file_path="", file_name="", **kwargs):
        """
        nginx文件上传回调
        :param account: 上传账号
        :param apply_sorder: 上传的子申请帮助订单id
        :param pay_msg:  支付消息
        :param file_path: 上传的文件路径
        :param file_name: 上传的文件名
        :param kwargs:  其他参数
        :return:
        """
        apply_help_pay_dic = ApplyHelpPayMgr().get_data_by_sorder(apply_sorder)
        apply_help_dic = ApplyHelpMgr().get_data_by_order(apply_help_pay_dic['apply_order'])
        if apply_help_dic['apply_uid'] != account.id:
            logger.info("apply_help_paid ERROR_LOGIC, apply_uid not valid, apply_uid:%s, id:%s" % (apply_help_dic['apply_uid'], account.id))
            self.set_status(error_code.ERROR_LOGIC, 'Parameter Error')
            return {"result": error_code.ERROR_LOGIC}

        if apply_help_pay_dic['apply_pstat'] != APYS_PAY_WAIT:
            logger.warn("apply_help_paid ERROR_LOGIC, apply stat is not APYS_PAY_WAIT, apply_uid:%s, id:%s" % (apply_help_dic['apply_uid'], account.id))
            self.set_status(error_code.ERROR_LOGIC, 'Parameter Error')
            return {"result": error_code.ERROR_LOGIC}

        if file_path:
            suffix = file_name.split(".")[1]

            new_file_name = "%s_%s.%s" % (account.id,
                                          urllib2.quote(time.strftime("%Y_%m_%d_%H_%M_%S", time.localtime(time.time()))),
                                          suffix)

            # 将nginx临时上传文件移动到存储路径
            mv_pay_pic(file_path, new_file_name, ArgumentParser().args.pic_store_path)

            cur_piture_link_path = ArgumentParser().args.pic_download_path + new_file_name
        else:
            cur_piture_link_path = ""
        ApplyHelpPayMgr().do_pay(apply_sorder, cur_piture_link_path, pay_msg)
        return {"result": error_code.ERROR_SUCCESS,
                "apply_help": {"apply_sorder": apply_sorder, "apply_pstat": apply_help_pay_dic['apply_pstat']}}

