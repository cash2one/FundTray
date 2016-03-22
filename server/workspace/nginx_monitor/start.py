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

from nginx_monitor import setting
from utils.service_control.controller import MainService
from utils.service_control.parser import parser_boolean


class Service(MainService):
    """
    主服务
    """
    def __init__(self):
        super(Service, self).__init__(setting.SERVICE_TYPE,
                                      setting.VERSION,
                                      is_sm=True)

    def services(self, args, thread_ls):
        """
        添加服务接口
        :param args: 参数变量
        :param thread_ls: 现有的服务列表
        :return:
        """
        from nginx_monitor.apps.web_app import WebApp
        thread_ls.append(WebApp(args.http_port, args.is_https))

    def add_cmd_opts(self, arg_parser):
        """
        在获取sm参数之前，提供添加arg_parser参数接口
        :param arg_parser: 参数变量
        :return:
        """
        arg_parser.add_argument('--is_https', default=False, type=parser_boolean,  help="Is use http ssl connection")
        arg_parser.add_argument('--http_port', default=80, type=int, help="The port of the service")


if __name__ == "__main__":
    import sys
    reload(sys)
    sys.setdefaultencoding('utf8')
    Service().start_service()