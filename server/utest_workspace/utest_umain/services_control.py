#!/usr/bin/python2.7
# coding=utf-8
"""
Created on 2015-5-7

@author: Jay
"""

import os
from utils.service_control.processer import start_process, stop_process
import time
from utils.service_control.caster import BEAT_INTERVAL
from utils.service_control.checker import HEARTBEAT_EXPIRE_TIME
from utils import logger
from utils.service_control.setting import SERVICE_TYPE, ST_SERVICE_MGR

cur_file_path = os.path.dirname(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))
service_mgr_path = os.path.join(cur_file_path, "workspace", "common_server", "service_mgr", "start.py")

logic_service_paths = [os.path.join(cur_file_path, "workspace", service, "start.py")
                       for service in SERVICE_TYPE
                       if service != ST_SERVICE_MGR]

mmm_da_start_path = logic_service_paths[0]

def start_service_mgr():
    start_process(service_mgr_path, "--db_host 10.24.6.7 --db_password !System")
    #start_process(service_mgr_path)

def stop_service_mgr():
    stop_process(service_mgr_path)

def restart_service_mgr():
    stop_service_mgr()
    start_service_mgr()

def start_logic_services():
    # start_process(mmm_da_start_path, "--apply_req second_1 --match second_11 --apply_pay second_21 --accept_req second_31 --day_seconds 1 --force_mtype user --enable_active False --enable_seal False --enable_pay_check False  --use_system_balance False")
    start_process(mmm_da_start_path, "--apply_req second_1 --match second_11 --apply_pay second_21 --accept_req second_31 --day_seconds 1 --force_mtype user --enable_active False --enable_pay_check False  --use_system_balance False")
    logger.warn("sleep %ss for service_mgr heartbeat:%s!!!" % (BEAT_INTERVAL, mmm_da_start_path))
    time.sleep(BEAT_INTERVAL)

def stop_logic_services():
    stop_process(mmm_da_start_path)
    time.sleep(1)

def restart_logic_services():
    stop_logic_services()
    start_logic_services()


def restart_services():
    stop_services()
    start_services()

def start_services():
    start_service_mgr()
    sm_sleep_time = HEARTBEAT_EXPIRE_TIME + 10
    logger.warn("sleep %ss for service_mgr check dead service!!!" % sm_sleep_time)
    time.sleep(sm_sleep_time)
    start_logic_services()

def stop_services():
    stop_logic_services()
    stop_service_mgr()