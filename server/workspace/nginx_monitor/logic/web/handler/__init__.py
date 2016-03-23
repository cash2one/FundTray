#!/usr/bin/python2.7
# coding=utf-8
"""
Created on 2015-4-28

@author: Jay
"""
from utils.route import route
from utils.network.http import HttpRpcHandler
from utils.wapper.web import web_adaptor
from utils.service_control.setting import PT_HTTPS, PT_HTTP
from utils.service_control.cacher import ServiceMgrCacher
from utils.interfaces.mmm_da.http_rpc import apply_help_paid
from mmm_da.setting import SERVICE_TYPE as ST_MMM_DA


MMMDAHttpRpcClt = ServiceMgrCacher().get_connection(ST_MMM_DA, protocol=PT_HTTPS)
if not MMMDAHttpRpcClt:
    MMMDAHttpRpcClt = ServiceMgrCacher().get_connection(ST_MMM_DA, protocol=PT_HTTP)
assert MMMDAHttpRpcClt


@route(r'/apply_help_pay', name='apply_help_pay')
class ApplyHelpPayHandler(HttpRpcHandler):
    @web_adaptor()
    def post(self, id, access_token, apply_sorder, pay_msg="", file="", **kwargs):
        """
        nginx文件上传回调
        :param access_token: 访问码
        :param apply_sorder: 上传的子申请帮助订单id
        :param pay_msg:  支付消息
        :param file: 上传的文件
        :return:
        """
        return apply_help_paid(MMMDAHttpRpcClt, id, access_token, apply_sorder, pay_msg, "", "")

