#!/usr/bin/python2.7
# coding=utf-8
"""
Created on 2015-5-26

@author: Jay
"""
import copy
import traceback
import datetime
import random
import platform
from collections import defaultdict
import ujson
from utils.meta.singleton import Singleton
from service_mgr.lib.service_group import ServiceGrpMgr
from service_mgr.lib.grant_machine import GrantMachineMgr
from utils import logger
from utils.scheduler import Jobs
from utils.interfaces.common import IManager
from utils.data.cache.dirty import DirtyFlagProcess
from service_mgr.db.db_oper import DBServiceInst
from utils.comm_func import datetime_to_string
from utils.service_control.setting import RT_HASH_RING, RT_CPU_USAGE_RDM, SS_RUNNING, SS_FREE, SERVICE_STATE
from utils.service_control.checker import HEARTBEAT_EXPIRE_TIME
from service_mgr.lib.filter_result import FilterServiceObjNotKeyResult, FilterServiceDicKeyGrpResult, FilterResult
from service_cluster import ServiceCluster
from service_mgr.logic.rpc.sender.cs_to_gs import GsRpcClient
from utils.wapper.catch import except_adaptor
from utils.service_control.setting import RT_MYSQL, PT_TCP
from utils.data.db import mysql_util
from service_mgr.lib.filter_result import FilterTPServiceNotKeyResult


MYSQL_DB_BACKUP_HOUR = 2
class Service(object):
    def __init__(self, id, ip, service_group, port, params, state, start_time, db_update_fun=None):
        self.id = id
        self.ip = ip
        self.service_group = service_group
        self._port = port
        self.params = params
        self.state = state
        self.start_time = start_time

        self.set_hb_info(heartbeat_time="")

        self.db_update_fun = db_update_fun
        self.tp_service_dic = {}
        self.dfp = DirtyFlagProcess(self)

        self._control_rpc = None

        Jobs().add_interval_job(HEARTBEAT_EXPIRE_TIME, self._heart_beat_expire)

        if "db_name" in self.params:
            Jobs().add_cron_job(self.__backup,hour=MYSQL_DB_BACKUP_HOUR)

    def set_hb_info(self, process_name="", service_version="unknown", port=None, current_load=1, heartbeat_time=None):
        """
        init heartbeat info
        :return:
        """
        self.process_name = process_name
        self.service_version = service_version
        self.current_load = current_load
        self._hb_port = port
        self.heartbeat_time = heartbeat_time if heartbeat_time is not None else datetime.datetime.now()
        self.gen_view_info()

    def gen_view_info(self):
        is_https = 'https' in self.get_port()
        http_proctol = "https" if is_https else "http"
        http_host = self.ip + ":" + str(self.get_port()['https'] if is_https else self.get_port()['http'])

        self.href_doc = http_host
        self.href = "%s://%s/doc" % (http_proctol, self.href_doc)
        jid = self.params.get("JID", None)
        self.locate = {http_proctol: http_host, "xmpp": "%s" % jid} \
            if jid \
            else {http_proctol: http_host}

    @property
    def control_rpc(self):
        tcp_port = self.get_port().get('tcp', None)
        if tcp_port:
            self._control_rpc = GsRpcClient(self.ip, tcp_port)
        return self._control_rpc

    def update(self, curtime):
        dirty_db_dict = self.dfp.get_db_dirty_attr()
        if dirty_db_dict and self.db_update_fun:
            dirty_db_dict['id'] = self.id
            self.db_update_fun([dirty_db_dict])

    def __str__(self):
        return str(self.__dict__)

    def __eq__(self, other):
        return self.id == other.id

    def get_port(self):
        return self._hb_port if self._hb_port else self._port

    def get_info_dic(self):
        return {"id": self.id,
                "ip": self.ip,
                "service_group": self.service_group,
                "port": self.get_port(),
                "params": self.params,
                "state": self.state,
                "start_time": self.start_time,
                "heartbeat_time": self.heartbeat_time,
                "service_version": self.service_version,
                "current_load": self.current_load,
                "href_doc": self.href_doc,
                "href": self.href,
                "locate": self.locate}

    def web_pick(self):
        heartbeat_time = datetime_to_string(self.heartbeat_time) \
            if isinstance(self.heartbeat_time, datetime.datetime) \
            else self.heartbeat_time

        start_time = datetime_to_string(self.start_time) \
            if isinstance(self.start_time, datetime.datetime) \
            else self.start_time

        return {"id": self.id,
                "ip": self.ip,
                "service_group": self.service_group,
                "port": self.get_port(),
                "params": self.params,
                "state": self.state,
                "start_time": start_time,
                "heartbeat_time": heartbeat_time,
                "process_name": self.process_name,
                "service_version": self.service_version,
                "current_load": self.current_load,
                "href_doc": self.href_doc if self.state == SS_RUNNING else "",
                "href": self.href if self.state == SS_RUNNING else ""}

    def _use(self):
        self._set_state(SS_RUNNING)

    def _free(self):
        if self.state == SS_FREE:
            return
        self._set_state(SS_FREE)
        self.set_hb_info(heartbeat_time="")

    def _set_state(self, new_state):
        if new_state == self.state:
            return

        self.state = new_state
        self.dfp.add_db_flag("state", False)
        ServiceMgr().on_service_state_change(self)

    def _heart_beat_expire(self):
        if self.state == SS_RUNNING:
            if not self.heartbeat_time:
                self.stop()
                return
            expire_time = self.heartbeat_time + datetime.timedelta(seconds=HEARTBEAT_EXPIRE_TIME)
            now = datetime.datetime.now()
            if expire_time <= now:
                self.stop()

    def is_free(self):
        return self.state == SS_FREE

    def start(self):
        if not self.is_free():
            return False

        self._use()
        self.start_time = datetime.datetime.now()
        self.dfp.add_db_flag("start_time", False)
        return True

    def stop(self):
        if not self.state == SS_RUNNING:
            return True

        self._free()
        return True

    def heart_beat(self, process_name, service_version, port, current_load,  running):
        assert isinstance(port, dict)
        self.set_hb_info(process_name, service_version, port, current_load)
        self._set_state(SS_RUNNING) if running else self.stop()

    def hash_key(self):
        return self.id

    def __backup(self):
        mysql_table = self.params["db_name"]

        from service_mgr.lib.tp_service import TPServiceMgr
        mysql_ls = TPServiceMgr().filter_tp_services(FilterTPServiceNotKeyResult,RT_MYSQL)
        for mysql_dic in mysql_ls:
            mysql_ip = mysql_dic['ip']
            
            # 支持tcp/TCP
            try:
                mysql_port = mysql_dic['port'][PT_TCP.lower()]
            except:
                mysql_port = mysql_dic['port'][PT_TCP]
            mysql_user = mysql_dic['params']['db_user']
            mysql_passwd = mysql_dic['params']['db_password']

            mysql_util.MysqlUtil.db_dump(mysql_ip,
                                         mysql_port,
                                         mysql_user,
                                         mysql_passwd,
                                         mysql_table,
                                         use_gzip=True if platform.system() == 'Linux' else False)
            logger.info("Service::__backup success!!! mysql_ip:%s mysql_port:%s mysql_table:%s" %
                        (mysql_ip, mysql_port, mysql_table))



class ServiceMgr(IManager):
    __metaclass__ = Singleton

    def __init__(self):
        self.__id_to_service_dic = {}
        self.__state_service_dic = {}
        ServiceCluster.service_mgr = self
        self.__grp_srv_cluster = defaultdict(ServiceCluster)
        self.__init_data_ls = None

    def init(self, data_ls):
        self.__init_data_ls = data_ls
        self.__id_to_service_dic = {}
        self.__state_service_dic = {}
        self.__grp_srv_cluster = defaultdict(ServiceCluster)

        for dic in data_ls:
            dic.pop("doc", None)
            service_obj = Service(db_update_fun=DBServiceInst.update_ls, **dic)

            # add id_to_service_dic
            self.__id_to_service_dic[int(dic['id'])] = service_obj

            # add state_service_dic
            self.__state_service_dic.setdefault(service_obj.service_group, {})\
                .setdefault(service_obj.ip, {})\
                .setdefault(service_obj.state, {})[service_obj.hash_key()] = service_obj

            # add running_hash_ring
            if service_obj.state == SS_RUNNING:
                self.__grp_srv_cluster[service_obj.service_group].add_service(service_obj, is_init=True)

    def update(self, curtime):
        [service_obj.update(curtime) for service_obj in self.__id_to_service_dic.values()]

    def get_init_data_ls(self):
        return self.__init_data_ls

    def db_pick(self, data_ls):
        """
        db 序列化
        :param data_ls:
        :return:
        """
        pick_ls = copy.deepcopy(data_ls)
        for dic in pick_ls:
            dic["port"] = ujson.dumps(dic['port']) if dic['port'] else ""
            dic["params"] = ujson.dumps(dic['params']) if dic['params'] else ""
        return pick_ls

    def db_unpick(self, data_ls):
        """
        db 反序列化
        :param data_ls:
        :return:
        """
        un_pick_ls = copy.deepcopy(data_ls)
        for dic in un_pick_ls:
            dic["port"] = ujson.loads(dic['port']) if dic['port'] else {}
            dic["params"] = ujson.loads(dic['params']) if dic['params'] else {}
        return un_pick_ls

    def web_pick(self, service_grp=None):
        """
        web 序列化
        :return:
        """
        grp_services = self.filter_services(FilterServiceDicKeyGrpResult, service_grp, None, None)
        [grp_services.update({grp: self.db_pick(services)}) for grp, services in grp_services.items()]
        grp_counts = dict((grp, len(services)) for grp, services in grp_services.items())
        return grp_services, grp_counts

    def web_unpick(self, data_ls):
        """
        web 反序列化
        :param data_ls:
        :return:
        """
        unpick_ls = copy.deepcopy(data_ls)

        v_unpick_data_ls = []
        for data_dic in unpick_ls:
            try:
                data_dic["port"] = ujson.loads(data_dic['port']) if data_dic['port'] else {}
                data_dic["params"] = ujson.loads(data_dic['params']) if data_dic['params'] else {}
                data_dic['state'] = SS_RUNNING if data_dic['state'] == "连接" else SS_FREE

                if not GrantMachineMgr().get_machine(data_dic.get('ip', ""))\
                        or not data_dic['service_group'] \
                        or not ServiceGrpMgr().get_service_grp(data_dic['service_group'])\
                        or not int(data_dic['state']) in SERVICE_STATE:
                    logger.warn("ServiceMgr::web_unpick invalid params:%s" % data_dic)
                    continue

                # 去除临时数据
                del data_dic['process_name']
                del data_dic['service_version']
                del data_dic['current_load']
                del data_dic['heartbeat_time']
            except:
                logger.warn("ServiceMgr::web_unpick invalid params:%s %s" % (data_dic, traceback.format_exc()))
                raise

            v_unpick_data_ls.append(data_dic)
        return v_unpick_data_ls

    @except_adaptor(is_raise=False)
    def on_service_state_change(self, service_obj):
        if service_obj.state == SS_RUNNING:
            self.__grp_srv_cluster[service_obj.service_group].add_service(service_obj)
        else:
            self.__grp_srv_cluster[service_obj.service_group].del_service(service_obj)

        self.__state_service_dic.get(service_obj.service_group, {})\
            .get(service_obj.ip, {})\
            .get(not service_obj.state, {})\
            .pop(service_obj.hash_key(), None)

        self.__state_service_dic.setdefault(service_obj.service_group, {})\
            .setdefault(service_obj.ip, {})\
            .setdefault(service_obj.state, {})[service_obj.hash_key()] = service_obj

    def get_service_by_id(self, service_id):
        return self.__id_to_service_dic.get(service_id, None)

    def get_services_by_hash_keys(self, hash_keys):
        return [self.get_service_by_id(hash_key) for hash_key in hash_keys]

    def get_run_services(self, service_grp_id, rdm_type=RT_CPU_USAGE_RDM, rdm_param=1):
        """
        选择在线服务列表
        注意，由于是列表操作，所以返回的对象有可能为空
        :param service_grp_id:服务组id
        :param rdm_type: 随机类型
        :param rdm_param: 随机参数，RT_HASH_RING:列表, RT_RANDOM:整形，随机个数
        :return:[Obj,Obj,Obj,,,]
        """
        if rdm_type == RT_HASH_RING:
            if not isinstance(rdm_param, list):
                rdm_param = [rdm_param]
            return self.__grp_srv_cluster[service_grp_id].get_service_objs(rdm_param)
        else:
            running_hash_keys = []
            [running_hash_keys.extend(machine_state_dic.get(SS_RUNNING, {}).keys())
             for machine_state_dic in self.__state_service_dic.get(service_grp_id, {}).values()]
            selected_hash_keys = random.sample(running_hash_keys, int(rdm_param)) if running_hash_keys else []
            return self.get_services_by_hash_keys(selected_hash_keys)

    def filter_services(self, filter_result=FilterResult, service_grp_id=None, ip=None, state=None):
        """
        根据服务器组、IP和状态筛选满足条件的服务
        :param filter_result:结果返回方式
        :param service_grp_id: 服务器组/服务器组列表
        :param ip: IP/IP列表
        :param state:服务状态
        :return:
        """
        f_result = filter_result()

        if isinstance(service_grp_id, tuple):
            service_grp_id = list(service_grp_id)
        elif service_grp_id is not None and not isinstance(service_grp_id, list):
            service_grp_id = [service_grp_id]

        if isinstance(ip, tuple):
            ip = list(ip)
        elif ip is not None and not isinstance(ip, list):
            ip = [ip]

        [[[f_result.form(t_service_grp_id, t_ip, t_state, id_service_dic)
           for t_state, id_service_dic in state_service_dic.items()
           if state is None or t_state == state]
          for t_ip, state_service_dic in ip_service_dic.items()
          if ip is None or t_ip in ip]
         for t_service_grp_id, ip_service_dic in self.__state_service_dic.items()
         if service_grp_id is None or t_service_grp_id in service_grp_id]

        return f_result.result()

    def free_a_service(self, ip, service_grp_id):
        """
        随机释放一个服务
        :param ip: IP
        :param service_grp_id: 服务器ID
        :return:
        """
        logger.warn("ServiceMgr::free_a_service ip:%s, service_grp_id:%s" % (ip, service_grp_id))
        busy_service_objs = self.filter_services(FilterServiceObjNotKeyResult, service_grp_id, ip, SS_RUNNING)
        rdm_service_obj = random.choice(busy_service_objs)
        rdm_service_obj.stop()
        return rdm_service_obj