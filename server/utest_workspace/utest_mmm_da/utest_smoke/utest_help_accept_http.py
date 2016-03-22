#!/usr/bin/python2.7
# coding=utf-8
"""
Created on 2015-12-16

@author: Jay
"""
from lib.account import *
from utils.interfaces.mmm_da.http_rpc import apply_help, cur_apply_help, apply_help_paid, \
    accept_help, cur_accept_help, accept_help_notreceived, account
from mmm_da.lib.help_pay.setting import APYS_PAY_SUCCESS, APYS_PAY_UNUSUAL
from lib.help import apply_from_req_2_confirm_flow_auto, get_mafuluo, random_apply_money
from lib.setting import SYNC_WAIT_TIME


class HelpAcceptHttpRPCTest(unittest.TestCase):

    # 初始化工作
    def setUp(self):
        pass

    # 退出清理工作
    def tearDown(self):
        pass

    @unittest_adaptor()
    def test_http_rpc_system_accept_help_notreceived_normal(self):
        """
         接受帮助未收到
         注意：如果要测试以下流程，mmm_da需要开启以下模式--apply_req second_1 --match second_11 --apply_pay second_21 --accept_req second_31 --day_seconds 1 --force_mtype system --enable_active False --enable_seal False  --enable_pay_check False
        :return:
        """
        new_id, new_passwd = new_account()
        new_token = new_access_token(new_id, new_passwd)

        apply_from_req_2_confirm_flow_auto(self, new_id, new_passwd, new_token, pay_cfrm=False)

        # 申请帮助方:当前申请帮助列表
        cur_apply_help_result = cur_apply_help(MMMDAHttpRpcClt, new_id, new_token)
        print "cur_apply_help_result,", cur_apply_help_result, type(cur_apply_help_result)
        self.assertTrue(cur_apply_help_result["apply_help_ls"])

        # 申请帮助方:申请帮助支付所有订单
        for apply_help_info in cur_apply_help_result['apply_help_ls']:
            apply_sorder = apply_help_info['apply_sorder']
            apply_help_pay_result = apply_help_paid(MMMDAHttpRpcClt, new_id, new_token, apply_sorder, "pay_msg", "/file1/file2", "file_name.png")
            print "apply_help_pay_result,", apply_help_pay_result
            self.assertTrue(apply_help_pay_result['apply_help']['apply_sorder'] == apply_sorder)
            self.assertTrue(apply_help_pay_result['apply_help']['apply_pstat'] == APYS_PAY_SUCCESS)
            apply_sorder = apply_help_pay_result['apply_help']['apply_sorder']

            ## 睡3秒，算利息
            time.sleep(3)

            accept_uid = apply_help_info['accept_uid']
            self.assertTrue(accept_uid)
            accept_token = new_access_token(accept_uid, force_passwd)

            # 接受帮助方:申请帮助确认
            acp_help_notreceived_result = accept_help_notreceived(MMMDAHttpRpcClt, accept_uid, accept_token, apply_sorder)
            print "acp_help_notreceived_result,", acp_help_notreceived_result

            # 接受帮助方:当前接受帮助
            cur_accept_help_result1 = cur_accept_help(MMMDAHttpRpcClt, accept_uid, accept_token)
            for apply_help_dic in cur_accept_help_result1['apply_help_ls']:
                if apply_help_dic['apply_sorder'] == apply_sorder:
                    self.assertTrue(apply_help_dic['apply_pstat'] == APYS_PAY_UNUSUAL)

    @unittest_adaptor()
    def test_http_rpc_system_accept_help_finish_normal(self):
        """
         接受帮助完成转化成钱包余额
         注意：如果要测试以下流程，mmm_da需要开启以下模式--apply_req second_1 --match second_11 --apply_pay second_21 --accept_req second_31 --day_seconds 1 --force_mtype system --enable_active False --enable_seal False  --enable_pay_check False
        :return:
        """
        new_id, new_passwd = new_account()
        new_token = new_access_token(new_id, new_passwd)

        apply_from_req_2_confirm_flow_auto(self, new_id, new_passwd, new_token)

        view_account_result = account(MMMDAHttpRpcClt, new_id, new_token, new_id)
        print "view_account_result,", view_account_result
        self.assertTrue(view_account_result['result'] == error_code.ERROR_SUCCESS)
        self.assertTrue(view_account_result['account_info']["mafuluo"])

    @unittest_adaptor()
    def test_http_rpc_accept_can_apply_normal(self):
        """
        接受帮助的同时可以申请帮助
         注意：如果要测试以下流程，mmm_da需要开启以下模式--apply_req second_1 --match second_11 --apply_pay second_21 --accept_req second_31 --day_seconds 1 --force_mtype system --enable_active False --enable_seal False  --enable_pay_check False
        :return:
        """
        new_id, new_passwd = new_account()
        new_token = new_access_token(new_id, new_passwd)

        # 申请帮助完成
        apply_from_req_2_confirm_flow_auto(self, new_id, new_passwd, new_token)

        # 申请帮助方:申请接受帮助， 不允许
        aft_apply_mafuluo = get_mafuluo(new_id, new_token)
        accept_help_rsz = accept_help(MMMDAHttpRpcClt, new_id, new_token, random.randint(1, aft_apply_mafuluo))
        self.assertTrue(accept_help_rsz['accept_help'])
        print "accept_help_rsz,", accept_help_rsz

        # 申请帮助
        apply_money = random_apply_money(new_id)
        apply_help_result = apply_help(MMMDAHttpRpcClt, new_id, new_token, apply_money)
        self.assertTrue(apply_help_result['result'] == error_code.ERROR_SUCCESS)
        print "apply_help_result,",apply_help_result
