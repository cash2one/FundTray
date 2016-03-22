#!/usr/bin/python2.7
# coding=utf-8
"""
Created on 2015-6-3

@author: Jay
"""
from utils.network.udp import UdpServer
import ujson
from service_mgr.lib.service.service_main import ServiceMgr
from utils import logger


class HeartbeatApp(UdpServer):
    def __init__(self, port):
        super(HeartbeatApp, self).__init__(port)

    def handle(self, data, address):
        service_id, process_name,service_version, port, current_load, running = ujson.loads(data)
        service_obj = ServiceMgr().get_service_by_id(int(service_id))
        if not service_obj:
            logger.warn("HeartbeatApp:handle invalid service_id:%s" % service_id)
            return

        service_obj.heart_beat(process_name,service_version, port, int(current_load), bool(running))