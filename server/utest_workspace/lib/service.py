#!/usr/bin/python2.7
# coding=utf-8
"""
Created on 2015-6-4

@author: Jay
"""
from utils.service_control.cacher import ServiceMgrCacher
from utils.service_control.setting import ST_MMM_DA
from utils.service_control.setting import PT_HTTPS


# register
RgstTcpRpc = ServiceMgrCacher().get_connection(ST_MMM_DA)
RgstHttpRpc = ServiceMgrCacher().get_connection(ST_MMM_DA, protocol=PT_HTTPS)