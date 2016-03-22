#!/usr/bin/python2.7
# coding=utf-8
"""
Created on 2016-1-14

@author: Jay
"""
from lib.common import *
from utils.interfaces.mmm_da.http_rpc import set_notice, get_history_notice, system_info
from lib.account import MMMDAHttpRpcClt, admin0d_id, admin01_passwd, admin01_access_token


class GMNoticeHttpRPCTest(unittest.TestCase):

    # 初始化工作
    def setUp(self):
        pass

    # 退出清理工作
    def tearDown(self):
        pass

    @unittest_adaptor()
    def test_http_rpc_set_notice_nomal(self):
        # 获取当前系统通知
        system_info_result0 = system_info(MMMDAHttpRpcClt, admin0d_id, admin01_access_token)
        print "system_info_result0,", system_info_result0
        self.assertTrue(system_info_result0)
        before_set_notice = system_info_result0['notice']

        # 获取当前历史通知
        history_notices0 = get_history_notice(MMMDAHttpRpcClt, admin0d_id, admin01_passwd)
        print "history_notices0,",history_notices0
        history_notice_before_len = len(history_notices0)

        # 设置通知
        new_notice = "notice" + str(time.time())
        set_notice_result = set_notice(MMMDAHttpRpcClt, admin0d_id, admin01_passwd, new_notice)
        self.assertTrue(set_notice_result == new_notice)

        # 获取当前历史通知
        history_notices1 = get_history_notice(MMMDAHttpRpcClt, admin0d_id, admin01_passwd)
        print "history_notices1,",history_notices1
        history_notice_after_len = len(history_notices1)

        # 获取当前系统通知
        system_info_result1 = system_info(MMMDAHttpRpcClt, admin0d_id, admin01_access_token)
        print "system_info_result1,", system_info_result1
        self.assertTrue(system_info_result1)
        after_set_notice = system_info_result1['notice']

        # 数据判断
        self.assertTrue(before_set_notice in history_notices1)
        self.assertTrue(after_set_notice == new_notice)
        self.assertTrue(history_notice_after_len == history_notice_before_len+1)
