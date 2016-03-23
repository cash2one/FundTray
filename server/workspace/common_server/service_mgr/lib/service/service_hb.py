#!/usr/bin/python2.7
# coding=utf-8
"""
Created on 2016-3-23

@author: Jay
"""
import time
from utils import logger
from utils.scheduler import Jobs
from utils.service_control.checker import HEARTBEAT_EXPIRE_TIME
from utils.service_control.setting import SS_RUNNING


class ServiceHeartBeat(object):
    def __init__(self, service_obj):
        self.__service_obj = service_obj
        self.heartbeat_time = None
        Jobs().add_interval_job(HEARTBEAT_EXPIRE_TIME, self.__expire_check)

    def heart_beat(self, service_version, current_load, stat):
        self.__service_obj.service_version = service_version
        self.__service_obj.current_load = current_load
        self.__service_obj.set_state(SS_RUNNING) if stat else self.__service_obj.stop()
        self.__service_obj.gen_view_info()

        self.heartbeat_time = time.time()

    @property
    def hb_time(self):
        return self.heartbeat_time

    def __expire_check(self):
        if self.__service_obj.state == SS_RUNNING:
            if not self.heartbeat_time:
                self._expire()
                return
            expire_time = self.heartbeat_time + HEARTBEAT_EXPIRE_TIME
            if expire_time <= time.time():
                self._expire()

    def _expire(self):
        logger.warn("ServiceHeartBeat::_expire!!! service:%s will stop" % self.__service_obj.id)
        self.__service_obj.stop()
