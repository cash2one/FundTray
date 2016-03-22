#!/usr/bin/python2.7
# coding=utf-8
"""
Created on 2015-12-16

@author: Jay
"""
from lib.common import *
from utils.interfaces.mmm_da.http_rpc import summary
from utils import error_code
from lib.account import MMMDAHttpRpcClt, admin0d_id, admin01_access_token


class TeamHttpRPCTest(unittest.TestCase):

    # 初始化工作
    def setUp(self):
        pass

    # 退出清理工作
    def tearDown(self):
        pass

    @unittest_adaptor()
    def test_http_rpc_team_summary_nomal(self):
        summary_result = summary(MMMDAHttpRpcClt, admin0d_id, admin01_access_token)
        print "account_result,", summary_result
        self.assertTrue(summary_result['result'] == error_code.ERROR_SUCCESS)


