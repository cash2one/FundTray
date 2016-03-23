#!/usr/bin/python2.7
# coding=utf-8
"""
Created on 2016-3-23

@author: Jay
"""
from utils import logger
from utils.scheduler import Jobs

SERVICE_VERIFY_INTERVAL_SECONDS = 60
class ServiceVerify(object):
    def __init__(self, service_obj):
        self.__service_obj = service_obj
        Jobs().add_interval_job(SERVICE_VERIFY_INTERVAL_SECONDS, self.__verify)

    def _is_valid(self):
        try:
            is_valid = self.__service_obj.service_ctl.control_rpc.verify()
        except:
            is_valid = False
        return is_valid

    def __verify(self):
        is_valid = self._is_valid()
        if not is_valid:
            self._invalid()

    def _invalid(self):
        logger.warn("ServiceHeartBeat::_invalid!!! service:%s will stop" % self.__service_obj.id)
        self.__service_obj.stop()
