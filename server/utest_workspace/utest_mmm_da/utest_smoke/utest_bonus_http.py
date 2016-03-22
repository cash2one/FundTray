#!/usr/bin/python2.7
# coding=utf-8
"""
Created on 2016-1-15

@author: Jay
"""
from lib.account import *
from utils.interfaces.mmm_da.http_rpc import get_bonus_logs
from lib.help import apply_from_req_2_confirm_flow_auto


class BonusHttpRPCTest(unittest.TestCase):

    # 初始化工作
    def setUp(self):
        pass

    # 退出清理工作
    def tearDown(self):
        pass

    @unittest_adaptor()
    def test_http_rpc_bonus_18888_normal(self):
        """
        奖金奖励
         注意：如果要测试以下流程，mmm_da需要开启以下模式--apply_req second_1 --match second_11 --apply_pay second_21 --accept_req second_31 --day_seconds 1 --force_mtype system --enable_active False --enable_seal False  --enable_pay_check False
        :return:
        """
        new_id, new_passwd = new_account()
        print "new_id,", new_id
        new_token = new_access_token(new_id, new_passwd)

        apply_from_req_2_confirm_flow_auto(self, new_id, new_passwd, new_token)

        time.sleep(1)

        bonus_log_ls = []

        # 获取所有的日志
        page_idx = 1
        get_bonus_logs_result = get_bonus_logs(MMMDAHttpRpcClt, admin0d_id, admin01_access_token, page_idx)
        while get_bonus_logs_result['bonus_logs']:
            bonus_log_ls.extend(get_bonus_logs_result['bonus_logs'])
            page_idx += 1
            get_bonus_logs_result = get_bonus_logs(MMMDAHttpRpcClt, admin0d_id, admin01_access_token, page_idx)

        afct_uid_ls = map(lambda dic:dic['afct_uid'], bonus_log_ls)
        print "afct_uid_ls,", afct_uid_ls
        self.assertTrue(str(new_id) in afct_uid_ls)
