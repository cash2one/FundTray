#!/usr/bin/python2.7
# coding=utf-8
"""
Created on 2015-12-16

@author: Jay
"""
from lib.account import *
from utils.interfaces.mmm_da.http_rpc import apply_help, cur_apply_help,\
    accept_help, cur_accept_help, del_accept_help, del_apply_help
from lib.help import apply_from_req_2_confirm_flow, apply_from_req_2_confirm_flow_auto, get_mafuluo, random_apply_money
from lib.setting import SYNC_WAIT_TIME


class HelpHttpRPCTest(unittest.TestCase):

    # 初始化工作
    def setUp(self):
        pass

    # 退出清理工作
    def tearDown(self):
        pass

    @unittest_adaptor()
    def test_http_rpc_system_apply_help_normal(self):
        """
         申请帮助流程测试，
         注意：如果要测试以下流程，mmm_da需要开启以下模式--apply_req second_1 --match second_11 --apply_pay second_21 --accept_req second_31 --day_seconds 1 --force_mtype system --enable_active False --enable_seal False  --enable_pay_check False
        :return:
        """
        new_id, new_passwd = new_account()
        new_token = new_access_token(new_id, new_passwd)
        print "new_id,",new_id

        # 申请帮助方:申请提供帮助
        pre_apply_mafuluo = get_mafuluo(new_id, new_token)
        print "pre_apply_mafuluo,",pre_apply_mafuluo
        self.assertTrue(pre_apply_mafuluo == 0)

        apply_from_req_2_confirm_flow(self, new_id, new_passwd, new_token)

        aft_apply_mafuluo = get_mafuluo(new_id, new_token)
        print "aft_apply_mafuluo,",aft_apply_mafuluo
        self.assertTrue(aft_apply_mafuluo > pre_apply_mafuluo)

        # 申请帮助方:申请接受帮助
        accept_help_rsz = accept_help(MMMDAHttpRpcClt, new_id, new_token, random.randint(1, aft_apply_mafuluo))
        self.assertTrue(accept_help_rsz['accept_help'])
        print "accept_help_rsz,", accept_help_rsz

        # 申请帮助方:当前接受帮助
        cur_accept_help_result1 = cur_accept_help(MMMDAHttpRpcClt,new_id, new_token)
        print "cur_accept_help_result1,", cur_accept_help_result1
        self.assertTrue('accept_help' in cur_accept_help_result1)

        # 请求等待排队
        time.sleep(SYNC_WAIT_TIME)

        # 申请帮助方:当前接受帮助
        cur_accept_help_result2 = cur_accept_help(MMMDAHttpRpcClt,new_id, new_token)
        print "cur_accept_help_result2,", cur_accept_help_result2
        self.assertTrue('accept_help' in cur_accept_help_result2)
        self.assertTrue('apply_help_ls' in cur_accept_help_result2)

    @unittest_adaptor()
    def test_http_rpc_system_apply_help_reapply(self):
        """
         申请帮助流程测试，
         注意：如果要测试以下流程，mmm_da需要开启以下模式--apply_req second_1 --match second_11 --apply_pay second_21 --accept_req second_31 --day_seconds 1 --force_mtype system --enable_active False --enable_seal False  --enable_pay_check False
        :return:
        """
        new_id, new_passwd = new_account()
        new_token = new_access_token(new_id, new_passwd)

        apply_from_req_2_confirm_flow_auto(self, new_id, new_passwd, new_token)

        # 申请帮助方:申请帮助
        apply_money = random_apply_money(new_id)
        apply_help_result = apply_help(MMMDAHttpRpcClt, new_id, new_token, apply_money)
        self.assertTrue(apply_help_result['result'] == error_code.ERROR_SUCCESS)
        print "apply_help_result,",apply_help_result

    @unittest_adaptor()
    def test_http_rpc_system_apply_help_reaccept(self):
        """
         申请帮助流程测试，
         注意：如果要测试以下流程，mmm_da需要开启以下模式--apply_req second_1 --match second_11 --apply_pay second_21 --accept_req second_31 --day_seconds 1 --force_mtype system --enable_active False --enable_seal False  --enable_pay_check False
        :return:
        """
        new_id, new_passwd = new_account()
        new_token = new_access_token(new_id, new_passwd)
        print "test_http_rpc_system_apply_help_reaccept, new_id,",new_id

        apply_from_req_2_confirm_flow_auto(self, new_id, new_passwd, new_token)
        apply_from_req_2_confirm_flow_auto(self, new_id, new_passwd, new_token)

        cur_mafuluo = get_mafuluo(new_id, new_token)

        # 申请帮助方:申请接受帮助
        accept_help_rsz = accept_help(MMMDAHttpRpcClt, new_id, new_token, random.randint(1, cur_mafuluo))
        print "accept_help_rsz,", accept_help_rsz

    @unittest_adaptor()
    def test_http_rpc_system_apply_help_delete_normal(self):
        """
         申请帮助流程测试，
         注意：如果要测试以下流程，mmm_da需要开启以下模式--apply_req second_1 --match second_11 --apply_pay second_21 --accept_req second_31 --day_seconds 1 --force_mtype system --enable_active False --enable_seal False  --enable_pay_check False
        :return:
        """
        new_id, new_passwd = new_account()
        new_token = new_access_token(new_id, new_passwd)

        # 申请帮助方:申请帮助
        apply_money = random_apply_money(new_id)
        apply_help_result = apply_help(MMMDAHttpRpcClt, new_id, new_token, apply_money)
        self.assertTrue(apply_help_result['result'] == error_code.ERROR_SUCCESS)
        self.assertTrue(apply_help_result['apply_help_ls'])
        print "apply_help_result,",apply_help_result

        # 申请帮助方:当前申请帮助列表
        cur_apply_help_result0 = cur_apply_help(MMMDAHttpRpcClt, new_id, new_token)
        print "cur_apply_help_result0,", cur_apply_help_result0, type(cur_apply_help_result0)
        self.assertTrue(not cur_apply_help_result0['apply_help_ls'])
        self.assertTrue(cur_apply_help_result0['apply_help']['apply_money'] == apply_money)

        # 申请帮助方:删除申请帮助
        del_apply_help_result = del_apply_help(MMMDAHttpRpcClt, new_id, new_token, apply_help_result['apply_help_ls'][0]['apply_order'])
        print "del_apply_help_result,", del_apply_help_result

        # 申请帮助方:当前申请帮助列表
        cur_apply_help_result1 = cur_apply_help(MMMDAHttpRpcClt, new_id, new_token)
        print "cur_apply_help_result1,", cur_apply_help_result1, type(cur_apply_help_result1)
        self.assertTrue(not cur_apply_help_result1['apply_help'])

    @unittest_adaptor()
    def test_http_rpc_system_accept_help_delete_normal(self):
        """
         申请帮助流程测试，
         注意：如果要测试以下流程，mmm_da需要开启以下模式--apply_req second_1 --match second_11 --apply_pay second_21 --accept_req second_31 --day_seconds 1 --force_mtype system --enable_active False --enable_seal False  --enable_pay_check False
        :return:
        """
        new_id, new_passwd = new_account()
        new_token = new_access_token(new_id, new_passwd)

        apply_from_req_2_confirm_flow_auto(self, new_id, new_passwd, new_token)

        # 申请帮助方:申请接受帮助
        cur_mafuluo = get_mafuluo(new_id, new_token)
        accept_help_rsz = accept_help(MMMDAHttpRpcClt, new_id, new_token, random.randint(1, cur_mafuluo))
        self.assertTrue(accept_help_rsz['accept_help'])
        print "accept_help_rsz,", accept_help_rsz

        # 申请帮助方:删除接受帮助
        del_accept_help_result = del_accept_help(MMMDAHttpRpcClt, new_id, new_token, accept_help_rsz['accept_help']['accept_order'])
        print "del_accept_help_result,", del_accept_help_result

        # 申请帮助方:当前接受帮助
        cur_accept_help_result1 = cur_accept_help(MMMDAHttpRpcClt,new_id, new_token)
        print "cur_accept_help_result1,", cur_accept_help_result1
        self.assertTrue(not cur_accept_help_result1['accept_help'])
