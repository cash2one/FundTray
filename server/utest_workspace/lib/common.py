#!/usr/bin/python2.7
# coding=utf-8
"""
Created on 2015-5-21

@author: Jay
"""
from gevent import monkey
monkey.patch_all()

import site
import os
import ujson
import random
import time
import unittest
import uuid
import urllib
import platform
import sys
from pyxmpp2.jid import JID
import gevent
from gevent import threading

# remove unused utruner args
if len(sys.argv) >= 3:
    if "utrunner.py" in sys.argv[0]:
        sys.argv = sys.argv[1:-1]

cur_path = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
site.addsitedir(cur_path)
site.addsitedir(os.path.join(cur_path, "utest_common_server"))
site.addsitedir(os.path.join(os.path.dirname(cur_path), "workspace"))
site.addsitedir(os.path.join(os.path.dirname(cur_path), "workspace", "common_server"))

from utils import error_code, logger, crypto
logger.init_log("unittest", "unittest")

from utils.network.tcp import TcpRpcClient, TcpRpcServer,  TcpRpcHandler
from utils.network.http import HttpRpcServer, HttpRpcHandler, HttpRpcClient
from utils.wapper.web import web_adaptor
from utils.route import Route, route
from utils.meta.singleton import Singleton
from utils.crypto.sign import sign, checksign, Signer
from utils.service_control import setting as service_control_setting
from utils.service_control.cacher import ServiceMgrCacher, ParamCacher
from utils.service_control.setting import ST_MMM, ST_MMM_DA
from utils.setting import enum


from lib.common_fun import random_str
from lib.setting import SYNC_WAIT_TIME

from common_fun import unittest_adaptor