#!/usr/bin/python2.7
# coding=utf-8
"""
Created on 2015-6-6

@author: Jay
"""
from utils.network.tcp import TcpRpcClient
from utils.network.http import HttpRpcClient
from utils.meta.singleton import Singleton
from utils.service_control.setting import PT_HTTP, PT_HTTPS, PT_TCP, SM_TCP_PORT, RT_CPU_USAGE_RDM
from utils.interfaces.service_mgr.tcp_rpc import find_service, find_services, find_tp_service
from utils.service_control.parser import ArgumentParser
from utils.service_control.finder import get_cur_ip
from utils import logger

class ServiceMgrCacher(object):
    __metaclass__ = Singleton

    def __init__(self):
        self.connect_dic = {}

    @staticmethod
    def new_connection(ip, port, protocol=PT_TCP):
        """
        新连接
        :param ip:服务器ip
        :param port:服务器端口
        :param protocol:服务器协议
        """
        logger.warn("ServiceMgrCacher::new_connection %s %s:%s!!!" % (protocol, ip, port))
        if protocol == PT_TCP:
            return TcpRpcClient(str(ip), int(port))
        elif protocol == PT_HTTP:
            return HttpRpcClient(str(ip), int(port))
        elif protocol == PT_HTTPS:
            return HttpRpcClient(str(ip), int(port), True)
        else:
            return None

    @staticmethod
    def find_service(service_type, rdm_type=RT_CPU_USAGE_RDM, rdm_param=1):
        """
        从sm查找单个服务的详细信息
        :param service_type:服务类型,
        :param rdm_type:随机类型，0选择cpu使用率最低的；1一致性hash选择
        :param rdm_param:如果随机类型是0,参数整形,表示随机个数
                         如果随机类型是1,list形式,hash key 列表
        :param protocol:协议
        :return:ip,port
        """
        found_service = find_service(ParamCacher().sm_rpc,
                                     service_type,
                                     rdm_type,
                                     rdm_param)
        return found_service

    @staticmethod
    def find_port(service_type, rdm_type=RT_CPU_USAGE_RDM, rdm_param=1, protocol=PT_TCP):
        """
        从sm查找单个服务的端口信息
        :param service_type:服务类型,
        :param rdm_type:随机类型，0选择cpu使用率最低的；1一致性hash选择
        :param rdm_param:如果随机类型是0,参数整形,表示随机个数
                         如果随机类型是1,list形式,hash key 列表
        :param protocol:协议
        :return:ip,port
        """
        found_service = find_service(ParamCacher().sm_rpc,
                                     service_type,
                                     rdm_type,
                                     rdm_param)
        if not found_service:
            return None, None

        if protocol == PT_TCP:
            return found_service['ip'], found_service['port']['tcp']
        elif protocol == PT_HTTP:
            if 'http' not in found_service['port']:
                return None, None
            return found_service['ip'], found_service['port']['http']
        elif protocol == PT_HTTPS:
            if 'https' not in found_service['port']:
                return None, None
            return found_service['ip'], found_service['port']['https']
        else:
            return None, None

    @staticmethod
    def find_ports(service_type, rdm_type=RT_CPU_USAGE_RDM, rdm_param=1, protocol=PT_TCP):
        """
        从sm查找多个服务的端口信息
        :param service_type:服务类型,
        :param rdm_type:随机类型，0选择cpu使用率最低的；1一致性hash选择
        :param rdm_param:如果随机类型是0,参数整形,表示随机个数
                         如果随机类型是1,list形式,hash key 列表
        :param protocol:协议
        :return:{idx:(ip,port),,,}
        """
        found_services = find_services(ParamCacher().sm_rpc,
                                       service_type,
                                       rdm_type,
                                       rdm_param)
        assert found_services
        for idx, service_info in found_services.items():
            if protocol == PT_TCP:
                found_services[idx] = service_info['ip'], service_info['port']['tcp']
            elif protocol == PT_HTTP:
                found_services[idx] = service_info['ip'], service_info['port']['http']
            elif protocol == PT_HTTPS:
                found_services[idx] = service_info['ip'], service_info['port']['https']
            else:
                found_services[idx] = None, None
        return found_services

    @staticmethod
    def find_tp_service(service):
        return find_tp_service(ParamCacher().sm_rpc, service)

    def get_connection(self, service_type, rdm_type=RT_CPU_USAGE_RDM, rdm_param=1, protocol=PT_TCP):
        """
        获取服务连接：从sm获取服务信息，并连接相关服务端口
        :param service_type:服务类型,
        :param rdm_type:随机类型，0选择cpu使用率最低的；1一致性hash选择
        :param rdm_param:如果随机类型是0,参数整形,表示随机个数
                         如果随机类型是1,list形式,hash key 列表
        :param protocol:协议
        :return:connection
        """
        ip, port = ServiceMgrCacher.find_port(service_type, rdm_type, rdm_param, protocol)
        if not ip or not port:
            return None
        ckey = "%s:%s" % (ip, port)
        connection = self.connect_dic.get(ckey, None)
        if not connection:
            connection = ServiceMgrCacher.new_connection(ip, port, protocol)
            if connection:
                self.connect_dic[ckey] = connection
        return connection

    def get_connections(self, service_type, rdm_type=RT_CPU_USAGE_RDM, rdm_param=1, protocol=PT_TCP):
        """
        获取服务连接列表：从sm获取服务信息，并连接相关服务端口
        :param service_type:服务类型,
        :param rdm_type:随机类型，0选择cpu使用率最低的；1一致性hash选择
        :param rdm_param:如果随机类型是0,参数整形,表示随机个数
                         如果随机类型是1,list形式,hash key 列表
        :param protocol:协议
        :return:{connection:[idx1,idex2,,,],,,,}
        """
        dic = ServiceMgrCacher.find_ports(service_type, rdm_type, rdm_param, protocol)
        connections = {}
        for idx, service_info in dic.items():
            if service_info == (None, None):
                continue

            ckey = "%s:%s" % service_info
            connection = self.connect_dic.get(ckey, None)
            if not connection:
                connection = ServiceMgrCacher.new_connection(service_info[0], service_info[1], protocol)
                assert connection
                self.connect_dic[ckey] = connection
            idx_ls = connections.setdefault(connection,[])
            idx_ls.append(idx)
        return connections

    @staticmethod
    def redirect(request_hdl, service_type, url, rdm_type=RT_CPU_USAGE_RDM, rdm_param=1, protocol=PT_HTTPS):
        """
        HTTP 协议重定向
        :param RequestHandler:请求处理对象
        :param service_type: 服务类型
        :param rdm_type:随机类型，0选择cpu使用率最低的；1一致性hash选择
        :param rdm_param:如果随机类型是0,参数整形,表示随机个数
                         如果随机类型是1,list形式,hash key 列表
        :param url:URL
        :return:
        """
        ip, port = ServiceMgrCacher.find_port(service_type, rdm_type, rdm_param, protocol)
        full_url = "https" if protocol == PT_HTTPS else "http" + "://%s:%s/%s" % (ip, port, url)
        logger.warn("ServiceMgrCacher::redirect full_url:%s!!!" % (full_url))
        return request_hdl.redirect(full_url)


class ParamCacher(object):
    __metaclass__ = Singleton

    @property
    def sm_ip(self):
        return ArgumentParser().args.sm_ip

    @property
    def is_sm_local(self):
        return self.sm_ip == get_cur_ip()

    @property
    def sm_rpc(self):
        _sm_rpc = self.__dict__.get("_sm_rpc", None)
        if not _sm_rpc:
            self._sm_rpc = TcpRpcClient(self.sm_ip, SM_TCP_PORT)
            assert self._sm_rpc.ping()
        return self._sm_rpc

    @property
    def redis_client(self):
        return self.__dict__.get("_redis_client", None)

    @redis_client.setter
    def redis_client(self, redis_client):
        self.__dict__['_redis_client'] = redis_client

    @property
    def db_instance(self):
        return self.__dict__.get("_db_instance", None)

    @db_instance.setter
    def db_instance(self, db_instance):
        self.__dict__['_db_instance'] = db_instance

    @property
    def orm_engine(self):
        return self.__dict__.get("_orm_engine", None)

    @orm_engine.setter
    def orm_engine(self, orm_engine):
        self.__dict__['_orm_engine'] = orm_engine

