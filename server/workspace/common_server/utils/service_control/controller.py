#!/usr/bin/python2.7
# coding=utf-8
"""
Created on 2015-6-3

@author: Jay
"""
from utils.data.db_update import db_update
from utils.data.db.mysql_manual import DBInstance
from utils.data.cache import redis_client
from caster import ServiceAdvertiser
from handler import ExitHandler
from utils.scheduler import Jobs
from checker import PortChecker
from cacher import ParamCacher
from utils import logger
import gevent
from parser import ArgumentParser, parser_boolean
from finder import IpFinder, get_random_port
import traceback
import sys

UPDATE_INTERVAL = 0.5

class MainService(object):
    """
    服务启动管理配置模块
    """
    def __init__(self, service_type, service_version, is_sm=False, db_update_dir_path=None,
                 use_mysqldb=False, use_orm=False, use_redis=False):
        self.service_type = service_type
        self.service_version = service_version
        self.thread_ls = []
        self.is_sm = is_sm
        self.db_update_dir_path = db_update_dir_path
        self.use_mysqldb = use_mysqldb
        self.use_orm = use_orm
        self.use_redis = use_redis

        self.adv = None
        self.sm_rpc = None

        logger.init_log(self.service_type, self.service_type)
        ExitHandler().add_exit_handler(self.stop_service)

        arg_parser = ArgumentParser()
        p = arg_parser.get_argparser()

        p.add_argument('--is_https', default=False, type=parser_boolean,  help="Is use http ssl connection")
        p.add_argument('--http_port', default=0, type=int,  help="The port of the http app listen")
        p.add_argument('--tcp_port', default=0, type=int,  help="The port of of the tcp rpc app listen")

        p.add_argument('--service_type', default=service_type, type=str, help="The type of the service")
        p.add_argument('--service_version', default=use_redis, type=str,  help="The version of the service")
        p.add_argument('--is_sm', default=is_sm, type=bool,  help="Whether it is the service manager")
        p.add_argument('--db_update_dir_path', default=db_update_dir_path, type=str,  help="The dir for db update use")
        p.add_argument('--use_mysqldb', default=use_mysqldb, type=parser_boolean,  help="Whether to use the mysqldb lib")
        p.add_argument('--use_orm', default=use_orm, type=parser_boolean,  help="Whether to use the orm db lib")
        p.add_argument('--use_redis', default=use_redis, type=parser_boolean,  help="Whether to use the redis cache")

        p.add_argument('--logger_mask', default='0000', type=str, help="The logger mask em es fm fs")

        self.add_cmd_opts(p)

        IpFinder().is_extranet = arg_parser.args.is_extranet

        if not self.is_sm:
            self.add_cmd_opts_after_sm(p)

        if self.db_update_dir_path:
            self._db_update()
        if self.use_mysqldb:
            self._start_mysqldb()
        if self.use_redis:
            self._start_redis_client()

        args = arg_parser.args
        arg_parser.will_change = False

        self.prepare(args)
        self.init(args)
        logger.set_logger_level(args.logger_level)

    def prepare(self, args):
        """
        参数准备
        :param args: 参数变量
        :return:
        """
        args.http_port = get_random_port() if args.http_port == 0 else args.http_port
        args.tcp_port = get_random_port() if args.tcp_port == 0 else args.tcp_port

    def init(self, args):
        """
        初始化接口
        :param args: 参数变量
        :return:
        """
        pass

    def exit(self):
        """
        程序退出接口
        :return:
        """
        pass

    def add_cmd_opts(self, arg_parser):
        """
        在获取sm参数之前，提供添加arg_parser参数接口
        :param arg_parser: 参数变量
        :return:
        """
        pass

    def add_cmd_opts_after_sm(self, arg_parser):
        """
        在获取sm参数之后，提供添加arg_parser参数接口
        :param arg_parser: 参数变量
        :return:
        """
        pass

    def update(self):
        """
        更新接口
        :return:
        """
        pass

    def services(self, args, thread_ls):
        """
        添加服务接口
        :param args: 参数变量
        :param thread_ls: 现有的服务列表
        :return:
        """
        pass

    def start_service(self):
        """
        启动服务
        :return:
        """
        args = ArgumentParser().args
        try:
            Jobs().add_interval_job(UPDATE_INTERVAL, self.update)

            if not self.is_sm:
                port = {"tcp": args.tcp_port}
                port.update({"https": args.http_port} if args.is_https else {"http": args.http_port})
                self.adv = ServiceAdvertiser(self.service_type, port, args.jid if "jid" in args else "", self.service_version)
                self.adv.advertise()

            check_ports = {}
            if "tcp_port" in args:
                check_ports['tcp'] = args.tcp_port
            if "http_port" in args:
                if not args.is_https:
                    check_ports['http'] = args.http_port
                else:
                    check_ports['https'] = args.http_port
            PortChecker(check_ports).start()

            self.thread_ls.extend([Jobs()])

            self.services(args, self.thread_ls)

            logger.warn("start services for %s, args:%s" % (self.service_type, args))
            gevent.joinall([thread.start() for thread in self.thread_ls])
        except:
            logger.error(traceback.format_exc())
            sys.exit(0)

    def stop_service(self, *args):
        """
        退出服务
        :param args: 参数
        :return:
        """
        # 保存数据
        self.update()

        self.exit()

        if not self.is_sm:
            self.adv.notify_shutdown()
        [thread.stop() for thread in self.thread_ls]

    def _db_update(self):
        """
        db版本文件更新
        :return:
        """
        # 按版本更新数据库结构或数据
        assert db_update.main(ArgumentParser().args.db_host,
                              ArgumentParser().args.db_port,
                              ArgumentParser().args.db_name,
                              ArgumentParser().args.db_user,
                              ArgumentParser().args.db_password,
                              self.db_update_dir_path)

    def _start_mysqldb(self):
        """
        mysql db引擎开启
        :return:
        """
        db_instance = DBInstance(db_host=ArgumentParser().args.db_host,
                                 db_port=ArgumentParser().args.db_port,
                                 db_name=ArgumentParser().args.db_name,
                                 db_username=ArgumentParser().args.db_user,
                                 db_password=ArgumentParser().args.db_password,
                                 err_file=logger.fatal)
        db_instance.init()
        ParamCacher().db_instance = db_instance

    def _start_redis_client(self):
        """
        启动redis client
        :return:
        """
        rc = redis_client.RedisClient.instance(ArgumentParser().args.redis_ip,
                                               ArgumentParser().args.redis_port,
                                               ArgumentParser().args.redis_db)
        ParamCacher().redis_client = rc