#!/usr/bin/python2.7
# coding=utf-8
"""
Created on 2015-4-25

@author: Jay
"""
import site
import os
site.addsitedir(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))
site.addsitedir(os.path.join(os.path.dirname(os.path.dirname(os.path.realpath(__file__))), "common_server"))
from gevent import monkey
monkey.patch_all()

from mmm_da import setting
from utils.service_control.controller import MainService
from utils.service_control.setting import RT_MYSQL
import time
from utils.service_control.parser import parser_boolean


class Service(MainService):
    """
    主服务
    """
    def __init__(self):
        super(Service, self).__init__(setting.SERVICE_TYPE,
                                      setting.VERSION,
                                      db_update_dir_path=os.path.join(os.path.dirname(__file__), "db_update"),
                                      use_mysqldb=True)

    def init(self, args):
        from mmm_da.lib.lib_mgr import LibMgr
        LibMgr().init()

    def update(self):
        super(Service, self).update()
        cur_time = time.time()
        from mmm_da.lib.lib_mgr import LibMgr
        LibMgr().update(cur_time)

    def services(self, args, thread_ls):
        """
        添加服务接口
        :param args: 参数变量
        :param thread_ls: 现有的服务列表
        :return:
        """
        from mmm_da.apps.rpc_app import RpcApp
        from mmm_da.apps.web_app import WebApp

        thread_ls.append(RpcApp(args.tcp_port))
        thread_ls.append(WebApp(args.http_port, args.is_https))

    def add_cmd_opts(self, arg_parser):
        """
        在获取sm参数之前，提供添加arg_parser参数接口
        :param arg_parser: 参数变量
        :return:
        """
        arg_parser.add_argument('--apply_req', default="minute_1", type=str, help="申请帮助请求处理定时")
        arg_parser.add_argument('--match', default="minute_11", type=str, help="申请帮助匹配接受帮助处理定时")
        arg_parser.add_argument('--apply_pay', default="minute_21", type=str, help="申请帮助支付检测定时")
        arg_parser.add_argument('--accept_req', default="minute_31", type=str, help="接受帮助请求处理定时")
        arg_parser.add_argument('--apply_wait', default="second_41", type=str, help="接受帮助等待检测处理定时")
        arg_parser.add_argument('--day_seconds', default=86400, type=int, help="时间基数")
        arg_parser.add_argument('--enable_active', default=True, type=parser_boolean, help="是否开启账号激活功能")
        arg_parser.add_argument('--enable_seal', default=True, type=parser_boolean, help="是否开启账号封号功能")
        arg_parser.add_argument('--enable_pay_check', default=True, type=parser_boolean, help="是否开启支付到期检测")
        arg_parser.add_argument('--force_mtype', default="user", type=str, help="强制匹配类型:system, user")
        arg_parser.add_argument('--use_system_balance', default=True, type=parser_boolean, help="是否使用系统")

        arg_parser.add_argument('--pic_store_ip', default="localhost", type=str, help="支付截图存储主机")
        arg_parser.add_argument('--pic_store_port', default=22, type=int, help="支付截图存储端口")
        arg_parser.add_argument('--pic_store_user', default="ubuntu", type=str, help="支付截图存储用户名")
        arg_parser.add_argument('--pic_store_path', default="/tmp/FundTray/pay_screen_shot", type=str, help="支付截图存储路径")
        arg_parser.add_argument('--pic_download_path', default="http://52.77.234.86:20150/", type=str, help="支付截图下载路径")

        arg_parser.add_argument('--db_name', type=str,  help="db name")

        from utils.service_control.cacher import ServiceMgrCacher
        mysql_dic = ServiceMgrCacher.find_tp_service(RT_MYSQL)
        arg_parser.add_argument('--db_host', default=mysql_dic['ip'], type=str, help="The host of the db")
        arg_parser.add_argument('--db_port', default=mysql_dic['port']['tcp'], type=int, help="The port of the db")
        arg_parser.add_argument('--db_user', default=mysql_dic['params']['db_user'], type=str, help="The username of the db")
        arg_parser.add_argument('--db_password', default=mysql_dic['params']['db_password'], type=str, help="The password for the db user")


if __name__ == "__main__":
    import sys
    reload(sys)
    sys.setdefaultencoding('utf8')
    Service().start_service()