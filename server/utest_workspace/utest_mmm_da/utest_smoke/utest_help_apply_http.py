#!/usr/bin/python2.7
# coding=utf-8
"""
Created on 2015-12-16

@author: Jay
"""
from lib.account import *
from utils.interfaces.mmm_da.http_rpc import apply_help, accept_help, cur_apply_help, \
    apply_help_refuse,cur_accept_help, auto_match, add_accept_help, apply_help_paid, apply_help_list
from lib.help import apply_from_req_2_confirm_flow_auto, get_mafuluo, random_apply_money, add_apply_help
from mmm_da.lib.help_pay.setting import APYS_PAY_SUCCESS, APYS_PAY_REFUSE


class HelpApplyHttpRPCTest(unittest.TestCase):

    # 初始化工作
    def setUp(self):
        pass

    # 退出清理工作
    def tearDown(self):
        pass

    @unittest_adaptor()
    def test_http_rpc_apply_cannot_accept_normal(self):
        """
        申请帮助的同时不能接受帮助
         注意：如果要测试以下流程，mmm_da需要开启以下模式--apply_req second_1 --match second_11 --apply_pay second_21 --accept_req second_31 --day_seconds 1 --force_mtype system --enable_active False --enable_seal False  --enable_pay_check False
        :return:
        """
        new_id, new_passwd = new_account()
        new_token = new_access_token(new_id, new_passwd)

        # 申请帮助完成
        apply_from_req_2_confirm_flow_auto(self, new_id, new_passwd, new_token)

        # 申请帮助
        apply_money = random_apply_money(new_id)
        apply_help_result = apply_help(MMMDAHttpRpcClt, new_id, new_token, apply_money)
        self.assertTrue(apply_help_result['result'] == error_code.ERROR_SUCCESS)
        print "apply_help_result,",apply_help_result

        # 申请帮助方:申请接受帮助， 不允许
        aft_apply_mafuluo = get_mafuluo(new_id, new_token)
        self.assertRaises(Exception, accept_help, MMMDAHttpRpcClt, new_id, new_token, random.randint(1, aft_apply_mafuluo))

    @unittest_adaptor()
    def test_http_rpc_system_apply_help_rejust(self):
        """
         申请帮助拒绝支付流程测试，拒绝支付以后，申请帮助订单取消，接受帮助订单还原
         注意：如果要测试以下流程，mmm_da需要开启以下模式--apply_req second_1 --match second_11 --apply_pay second_21 --accept_req second_31 --day_seconds 1 --force_mtype system --enable_active False --enable_seal False --enable_pay_check False
        :return:
        """
        diff_from_apply_to_accept = random.randint(1, 3) * 1000
        print "diff_from_apply_to_accept,",diff_from_apply_to_accept
        # 申请帮助方
        apply_id, apply_passwd = new_account()
        apply_token = new_access_token(apply_id, apply_passwd)

        apply_money = random_apply_money(apply_id)
        print "apply_money,",apply_money
        add_apply_help_result = add_apply_help(MMMDAHttpRpcClt, admin0d_id, admin01_passwd, apply_id, apply_money)
        print "add_apply_help_result,", add_apply_help_result

        # 接受帮助方
        accept_id, accept_passwd = new_account()
        accept_token = new_access_token(accept_id, accept_passwd)
        accept_money = apply_money + diff_from_apply_to_accept
        print "accept_money,",accept_money
        add_accept_help_result = add_accept_help(MMMDAHttpRpcClt, admin0d_id, admin01_passwd, accept_id, accept_money)
        print "add_accept_help_result,", add_accept_help_result

        # 自动匹配
        auto_match_result = auto_match(MMMDAHttpRpcClt, admin0d_id, admin01_passwd, apply_id, accept_id, apply_money)
        self.assertTrue(auto_match_result == error_code.ERROR_SUCCESS)

        # 申请帮助方:当前申请帮助列表
        cur_apply_help_result = cur_apply_help(MMMDAHttpRpcClt, apply_id, apply_token)
        print "cur_apply_help_result,", cur_apply_help_result
        self.assertTrue(cur_apply_help_result['apply_help'])

        # 申请帮助方:当前支付订单肯定就一个，所有强制写死
        apply_help_info = cur_apply_help_result['apply_help_ls'][0]
        apply_sorder = apply_help_info['apply_sorder']
        assert str(apply_help_info['accept_uid']) == str(accept_id)

        # 接受帮助方:当前接受帮助, apply_help_ls存在, ['accept_help']['accept_lmoney'] == accept_lmoney
        cur_accept_help_result0 = cur_accept_help(MMMDAHttpRpcClt, accept_id, accept_token)
        print "cur_accept_help_result0,", cur_accept_help_result0
        self.assertTrue(cur_accept_help_result0['accept_help']['accept_lmoney'] == diff_from_apply_to_accept)
        self.assertTrue(cur_accept_help_result0['apply_help_ls'])

        # 申请帮助方:拒绝支付
        apply_help_refuse_rsz = apply_help_refuse(MMMDAHttpRpcClt, apply_id, apply_token, apply_sorder)
        print "apply_help_refuse_rsz,", apply_help_refuse_rsz

        # 接受帮助方:当前接受帮助, 订单状态变成拒绝支付, ['accept_help']['accept_lmoney']==['accept_help']['accept_money']
        cur_accept_help_result1 = cur_accept_help(MMMDAHttpRpcClt, accept_id, accept_token)
        print "cur_accept_help_result1,", cur_accept_help_result1
        self.assertTrue(cur_accept_help_result1['accept_help']['accept_lmoney'] ==
                        cur_accept_help_result1['accept_help']['accept_money'])
        self.assertTrue(cur_accept_help_result1['apply_help_ls'][0]['apply_pstat'] == APYS_PAY_REFUSE)

    @unittest_adaptor()
    def test_http_rpc_system_apply_paid_notmsg_notpiture_normal(self):
        """
         申请帮助请求-自动匹配-支付没有上传截图和留言流程，拒绝支付以后，申请帮助订单取消，接受帮助订单还原
         注意：如果要测试以下流程，mmm_da需要开启以下模式--apply_req second_1 --match second_11 --apply_pay second_21 --accept_req second_31 --day_seconds 1 --force_mtype system --enable_active False --enable_seal False --enable_pay_check False
        :return:
        """
        diff_from_apply_to_accept = 1000

        # 申请帮助方:信息
        apply_id, apply_passwd = new_account()
        apply_token = new_access_token(apply_id, apply_passwd)

        apply_money = random_apply_money(apply_id)
        add_apply_help_result = add_apply_help(MMMDAHttpRpcClt, admin0d_id, admin01_passwd, apply_id, apply_money)
        print "add_apply_help_result,", add_apply_help_result

        # 接受帮助方
        accept_id, accept_passwd = new_account()
        accept_token = new_access_token(accept_id, accept_passwd)

        accept_money = apply_money + diff_from_apply_to_accept
        add_accept_help_result = add_accept_help(MMMDAHttpRpcClt, admin0d_id, admin01_passwd, accept_id, accept_money)
        print "add_accept_help_result,", add_accept_help_result

        # 自动匹配
        auto_match_result = auto_match(MMMDAHttpRpcClt, admin0d_id, admin01_passwd, apply_id, accept_id, apply_money)
        self.assertTrue(auto_match_result == error_code.ERROR_SUCCESS)
        accept_lmoney = accept_money - apply_money
        assert accept_lmoney == diff_from_apply_to_accept

        # 申请帮助方:当前申请帮助列表
        cur_apply_help_result = cur_apply_help(MMMDAHttpRpcClt, apply_id, apply_token)
        print "cur_apply_help_result,", cur_apply_help_result, type(cur_apply_help_result)
        self.assertTrue(cur_apply_help_result["apply_help_ls"])

        # 申请帮助方:申请帮助支付所有订单
        for apply_help_info in cur_apply_help_result['apply_help_ls']:
            apply_sorder = apply_help_info['apply_sorder']
            apply_help_pay_result = apply_help_paid(MMMDAHttpRpcClt, apply_id, apply_token, apply_sorder, "", "", "")
            print "apply_help_pay_result,", apply_help_pay_result
            self.assertTrue(apply_help_pay_result['apply_help']['apply_sorder'] == apply_sorder)
            self.assertTrue(apply_help_pay_result['apply_help']['apply_pstat'] == APYS_PAY_SUCCESS)