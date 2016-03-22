#!/usr/bin/python2.7
# coding=utf-8
"""
Created on 2015-4-27

@author: Jay
"""
from utils.network.tcp import TcpRpcHandler
from utils.wapper.stackless import gevent_adaptor
from utils.wapper.tcp import tcp_recv_adaptor, tcp_send_adaptor
from utils import error_code
from service_mgr.lib.service.service_main import ServiceMgr, SS_FREE
from service_mgr.lib.service_group import ServiceGrpMgr
from service_mgr.lib.grant_machine import GrantMachineMgr
from service_mgr.lib.tp_service import TPServiceMgr
from service_mgr.lib.filter_result import FilterServiceObjNotKeyResult, FilterServiceDicKeyGrpResult, \
    FilterTPServiceNotKeyResult, FilterTPServiceKeyGrpResult
import random
from service_mgr.logic.rpc import TCP_SIGN
from utils import logger
import platform
from utils.wapper.crypto import sign_checker
from utils.service_control.setting import RT_CPU_USAGE_RDM, RT_HASH_RING


class TcpHandler(TcpRpcHandler):

    @gevent_adaptor()
    @tcp_send_adaptor()
    @tcp_recv_adaptor()
    @sign_checker()
    def start_service(self, service_type, ip):
        """
        启动服务
        :param service_type:服务类型
        :param ip:IP
        :return:
        """
        if not ServiceGrpMgr().get_service_grp(service_type)\
                or not GrantMachineMgr().get_machine(ip):
            logger.error("TcpHandler::start_service Failed!!!, ERROR_PARAMS_ERROR, service_type:%s ip:%s"
                         % (service_type, ip))
            return {"result": error_code.ERROR_PARAMS_ERROR}

        service_obj_ls = ServiceMgr().filter_services(FilterServiceObjNotKeyResult, service_type, ip, SS_FREE)

        # windows 系统特殊处理，由于windows无法接收进程退出事件,一台windows只能启动一个进程
        if not service_obj_ls and platform.system() != 'Linux':
            service_obj_ls = [ServiceMgr().free_a_service(ip, service_type)]

        if not service_obj_ls:
            logger.error("TcpHandler::start_service Failed!!!, not free services, service_type:%s ip:%s"
                         % (service_type, ip))
            return {"result": error_code.ERROR_SERVICE_START_ERROR}

        select_service_obj = random.choice(service_obj_ls)
        if not select_service_obj.start():
            logger.error("TcpHandler::start_service Failed!!!, ERROR_SERVICE_START_ERROR, service_type:%s ip:%s"
                         % (service_type, ip))
            return {"result": error_code.ERROR_SERVICE_START_ERROR}

        return {"result": error_code.ERROR_SUCCESS,
                "service_info": select_service_obj.get_info_dic(),
                "sign": TCP_SIGN}

    @gevent_adaptor()
    @tcp_send_adaptor()
    @tcp_recv_adaptor()
    @sign_checker()
    def stop_service(self, service_id):
        """
        停止服务
        :param service_id:服务ID
        :param sign: 请求服务器的签名
        :return:
        """
        service_obj = ServiceMgr().get_service_by_id(service_id)
        if not service_obj:
            logger.error("TcpHandler::stop_service Failed!!!, ERROR_SERVICE_START_ERROR, service_id:%s"
                         % (service_id))
            return {"result": error_code.ERROR_PARAMS_ERROR}

        if not service_obj.stop():
            return {"result": error_code.ERROR_SERVICE_STOP_ERROR}

        logger.error("TcpHandler::stop_service success!!!, service_id:%s" % service_id)
        return {"result": error_code.ERROR_SUCCESS,
                "sign": TCP_SIGN}

    @gevent_adaptor()
    @tcp_send_adaptor()
    @tcp_recv_adaptor()
    @sign_checker()
    def find_service(self, service_type, rdm_type=RT_CPU_USAGE_RDM, rdm_param=1):
        """
        查找对应一个服务
        :param service_type:服务类型
        :param rdm_type:随机类型，0选择cpu使用率最低的；1一致性hash选择
        :param rdm_param:如果随机类型是0,参数整形,表示随机个数
                         如果随机类型是1,list形式,hash key 列表
        :return:
        """
        if rdm_type == RT_HASH_RING and not isinstance(rdm_param, list):
            rdm_param = [rdm_param]

        if not ServiceGrpMgr().get_service_grp(service_type):
            logger.error("TcpHandler::find_service Failed!!!, ERROR_PARAMS_ERROR, service_type:%s" % service_type)
            return {}

        service_obj_ls = ServiceMgr().get_run_services(service_type, rdm_type, rdm_param)
        if not service_obj_ls:
            return {}

        select_service_obj = service_obj_ls[0]
        if not select_service_obj:
            return {}

        return {"ip": select_service_obj.ip,
                "port": select_service_obj.get_port(),
                "jid": select_service_obj.params.get("JID", ""),
                "jid_pwd": select_service_obj.params.get("JID_PWD", "")}

    @gevent_adaptor()
    @tcp_send_adaptor()
    @tcp_recv_adaptor()
    @sign_checker()
    def find_services(self, service_type, rdm_type=RT_CPU_USAGE_RDM, rdm_param=1):
        """
        查找服务列表
        :param service_type:服务类型
        :param rdm_type:随机类型，0选择cpu使用率最低的；1一致性hash选择
        :param rdm_param:如果随机类型是0,参数整形,表示随机个数
                         如果随机类型是1,list形式,hash key 列表
        :return:
        """
        if rdm_type == RT_HASH_RING and not isinstance(rdm_param, list):
            rdm_param = [rdm_param]

        if not ServiceGrpMgr().get_service_grp(service_type):
            logger.error("TcpHandler::find_service Failed!!!, ERROR_PARAMS_ERROR, service_type:%s" % service_type)
            return {}

        service_obj_ls = ServiceMgr().get_run_services(service_type, rdm_type, rdm_param)
        if not service_obj_ls:
            return {}

        result = {}
        for idx, service_obj in enumerate(service_obj_ls):
            result_key = idx if rdm_type == RT_CPU_USAGE_RDM else rdm_param[idx]
            result[result_key] = {"ip": service_obj.ip,
                                  "port": service_obj.get_port(),
                                  "jid": service_obj.params.get("JID",""),
                                  "jid_pwd": service_obj.params.get("JID_PWD", "")}
        return result

    @gevent_adaptor()
    @tcp_send_adaptor()
    @tcp_recv_adaptor()
    @sign_checker()
    def find_tp_service(self, service):
        """
        查找一个资源:
        :param service:第三方服务名称
        :return:
        """
        # 注意：此函数需要集群处理
        all_tp_service_ls = TPServiceMgr().filter_tp_services(FilterTPServiceNotKeyResult, service)
        return random.choice(all_tp_service_ls) if all_tp_service_ls else None

    @gevent_adaptor()
    @tcp_send_adaptor()
    @tcp_recv_adaptor()
    @sign_checker()
    def view_logic_services(self, viewer, state=None):
        """
        获取所有的服务，以group分组
        :param viewer: 请求者
        :param state: 需要的服务状态
        :return: {"grp":[service,,,,,],,,,}
        """
        return ServiceMgr().filter_services(FilterServiceDicKeyGrpResult,
                                            ServiceGrpMgr().get_visible(viewer),
                                            None,
                                            state)

    @gevent_adaptor()
    @tcp_send_adaptor()
    @tcp_recv_adaptor()
    @sign_checker()
    def view_tp_services(self, viewer):
        """
        获取tp服务组信息
        :param viewer: 请求者
        :return: {"grp":[service,,,,,],,,,}
        """
        return TPServiceMgr().filter_tp_services(FilterTPServiceKeyGrpResult,
                                                 ServiceGrpMgr().get_visible(viewer))
