#!/usr/bin/python2.7
# coding=utf-8
"""
Created on 2015-6-2

@author: Jay
"""
import argparse

from utils import error_code
from utils.logger import INFO
from utils.interfaces.service_mgr.tcp_rpc import start_service
from utils.meta.singleton import Singleton
from finder import get_cur_ip


def parser_boolean(b):
    if b in ['yes', 'y', '1', 'true', "True", "t", "T"]:
        return True
    if b in ['no', 'n', '0', 'false', "False", "f", "F"]:
        return False

class ArgumentParser(object):
    __metaclass__ = Singleton

    def __init__(self):
        self.argparser = argparse.ArgumentParser(conflict_handler='resolve')
        self._args = None
        self.will_change = True

        self.argparser.add_argument('--is_extranet', default=False, type=parser_boolean, help="The network type used: intranet or extranet")
        self.argparser.add_argument('--sm_ip', default=get_cur_ip(), type=str,  help="The ip of the service mgr service")
        self.argparser.add_argument('--is_https', default=True, type=parser_boolean,  help="Is use http ssl connection")
        self.argparser.add_argument('--logger_level', default=INFO, type=str,  help="Default logger level")

    def get_argparser(self):
        return self.argparser

    @property
    def args(self):
        if self.will_change or not self._args:
            self._args = self.argparser.parse_args()
        return self._args


class SMParamParser(object):
    __metaclass__ = Singleton

    def __init__(self, service_type, sm_rpc, arg_parser, rdm_port_fun=None):
        self.service_type = service_type
        self.sm_rpc = sm_rpc
        self.rdm_port_fun = rdm_port_fun
        self.result = None

        self.id = None
        self.port = None
        self.params = None

        self.req_sm_argument()

        self.add_service_args(arg_parser)
        self.add_port_args(arg_parser)
        self.add_jid_args(arg_parser)
        self.add_mysql_args(arg_parser)
        self.add_redis_args(arg_parser)

    def req_sm_argument(self):
        result = start_service(self.sm_rpc,
                               self.service_type,
                               get_cur_ip())
        assert result['result'] == error_code.ERROR_SUCCESS

        self.id = result['service_info']['id']
        self.port = result['service_info']['port']
        self.params = result['service_info']['params']

    def add_service_args(self, arg_parser):
        arg_parser.add_argument('--service_id', default=self.id, type=int,  help="The id of the service")

    def add_port_args(self, arg_parser):
        assert self.rdm_port_fun

        http_port = self.port.get("http", None)
        if http_port is not None:
            http_port = self.rdm_port_fun() if http_port == 0 else http_port
            arg_parser.add_argument('--is_https', default=False, type=parser_boolean,  help="Is use http ssl connection")
            arg_parser.add_argument('--http_port', default=http_port, type=int,  help="The port of the http app listen")
            self.port['http'] = http_port

        https_port = self.port.get("https", None)
        if https_port is not None:
            https_port = self.rdm_port_fun() if https_port == 0 else https_port
            arg_parser.add_argument('--http_port', default=https_port, type=int,  help="The port of the http app listen")
            self.port['https'] = https_port

        tcp_port = self.port.get("tcp", None)
        if tcp_port is not None:
            tcp_port = self.rdm_port_fun() if tcp_port == 0 else tcp_port
            arg_parser.add_argument('--tcp_port', default=tcp_port, type=int,  help="The port of of the tcp rpc app listen")
            self.port['tcp'] = tcp_port
        arg_parser.add_argument('--port', default=self.port, type=int,  help="The port dict of the service")


    def add_jid_args(self, arg_parser):
        jid = self.params.get("JID", None)
        if jid is not None:
            arg_parser.add_argument('--jid', default=jid, type=str,  help="The jid of the openfire for the service")
        jid_pwd = self.params.get("JID_PWD", None)
        if jid_pwd is not None:
            arg_parser.add_argument('--jid_pwd', default=jid_pwd, type=str,  help="The jid password for the jid")

    def add_mysql_args(self, arg_parser):
        db_name = self.params.get("db_name", None)
        if db_name is not None:
            arg_parser.add_argument('--db_name', default=db_name, type=str,  help="db name")

    def add_redis_args(self, arg_parser):
        redis_db = self.params.get("redis_db", None)
        if redis_db is not None:
            arg_parser.add_argument('--redis_db', default=redis_db, type=str,  help="redis db")