#!/usr/bin/python2.7
# coding=utf-8
"""
Created on 2015-12-16

@author: Jay
"""

from lib.common import *
from utils import error_code
from utils.interfaces.mmm_da.http_rpc import active
from lib.account import admin0d_id, admin01_passwd, admin01_access_token, MMMDAHttpRpcClt, new_account

class ActiveHttpRPCTest(unittest.TestCase):
    @unittest_adaptor()
    def test_http_rpc_active_nomal(self):
        new_id, new_passwd = new_account(can_active=False)

        active_result = active(MMMDAHttpRpcClt, admin0d_id, admin01_access_token, new_id)
        print "active_result,",active_result
        self.assertTrue(active_result == error_code.ERROR_SUCCESS)

