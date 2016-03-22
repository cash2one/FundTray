#!/usr/bin/python2.7
# coding=utf-8
"""
Created on 2015-12-16

@author: Jay
"""

from lib.account import *
from utils.interfaces.mmm_da.http_rpc import apply_help, cur_apply_help, apply_help_paid, accept_help_confirm,\
    cur_accept_help, account, add_accept_help, auto_match, add_apply_help
from mmm_da.lib.help_pay.setting import APYS_PAY_SUCCESS
from mmm_da.lib.help_req.setting import MAX_APPLY_HELP_MONEY, MIN_APPLY_HELP_MONEY

def random_apply_money(id, max_money=None):
    view_account_result = account(MMMDAHttpRpcClt, admin0d_id, admin01_access_token, id)
    print "view_account_result,",view_account_result
    assert view_account_result['result'] == error_code.ERROR_SUCCESS
    max_apply_money = view_account_result['account_info']['max_apply_money']
    max_apply_money = max_apply_money if max_apply_money >= MIN_APPLY_HELP_MONEY else MIN_APPLY_HELP_MONEY

    if max_money:
        assert max_money >= max_apply_money

    factor = max_money/1000 if max_money else 10
    apply_money = max_apply_money + 1000 * random.randint(1, factor)
    if apply_money > MAX_APPLY_HELP_MONEY:
        apply_money = MAX_APPLY_HELP_MONEY
    return apply_money


def apply_from_req_2_confirm_flow(utest_obj, apply_id, apply_passwd, apply_token):
    """
    请求-匹配-支付-确认完整流程
    :param utest_obj:
    :param apply_id:
    :param apply_passwd:
    :param apply_token:
    :return:
    """
    apply_money = random_apply_money(apply_id)
    # 申请帮助方:申请帮助
    apply_help_result = apply_help(MMMDAHttpRpcClt, apply_id, apply_token, apply_money)
    utest_obj.assertTrue(apply_help_result['result'] == error_code.ERROR_SUCCESS)
    utest_obj.assertTrue(apply_help_result['apply_help_ls'])
    print "apply_help_result,",apply_help_result

    # 申请帮助方:当前申请帮助列表
    cur_apply_help_result0 = cur_apply_help(MMMDAHttpRpcClt, apply_id, apply_token)
    print "cur_apply_help_result0,", cur_apply_help_result0, type(cur_apply_help_result0)
    utest_obj.assertTrue(cur_apply_help_result0['apply_help'])

    # 申请帮助方:再次申请帮助
    utest_obj.assertRaises(Exception, apply_help, MMMDAHttpRpcClt, apply_id, apply_token, apply_money)

    # 请求等待排队
    time.sleep(SYNC_WAIT_TIME)

    # 申请帮助方:再次申请帮助
    utest_obj.assertRaises(Exception, apply_help, MMMDAHttpRpcClt, apply_id, apply_token, apply_money)

    paid_confirm(utest_obj, apply_id, apply_token)



def apply_from_req_2_confirm_flow_auto(utest_obj, apply_id, apply_passwd, apply_token, pay_cfrm=True):
    """
    请求-自动匹配-支付-确认完整流程
    :param utest_obj:
    :param apply_id:
    :param apply_passwd:
    :param apply_token:
    :param pay_cfrm:是否确认支付,默认True
    :return:
    """
    apply_money = random_apply_money(apply_id)
    # 接受帮助方
    accept_id, accept_passwd = new_account()
    add_accept_help_result = add_accept_help(MMMDAHttpRpcClt, admin0d_id, admin01_passwd, accept_id, apply_money)
    print "add_accept_help_result,", add_accept_help_result

    # 申请帮助方
    add_apply_help_result = add_apply_help(MMMDAHttpRpcClt, admin0d_id, admin01_passwd, apply_id, apply_money)
    print "add_apply_help_result,", add_apply_help_result

    # 自动匹配
    auto_match_result = auto_match(MMMDAHttpRpcClt, admin0d_id, admin01_passwd, apply_id, accept_id, apply_money)
    utest_obj.assertTrue(auto_match_result == error_code.ERROR_SUCCESS)
    if pay_cfrm:
        paid_confirm(utest_obj, apply_id, apply_token)


def paid_confirm(utest_obj, apply_id, apply_token):
    # 申请帮助方:当前申请帮助列表
    cur_apply_help_result = cur_apply_help(MMMDAHttpRpcClt, apply_id, apply_token)
    print "cur_apply_help_result,", cur_apply_help_result, type(cur_apply_help_result)
    utest_obj.assertTrue(cur_apply_help_result["apply_help_ls"])

    # 申请帮助方:申请帮助支付所有订单
    for apply_help_info in cur_apply_help_result['apply_help_ls']:
        apply_sorder = apply_help_info['apply_sorder']

        apply_help_pay_result = apply_help_paid(MMMDAHttpRpcClt, apply_id, apply_token, apply_sorder, "pay_msg", "/file1/file2", "file_name.png")
        print "apply_help_pay_result,", apply_help_pay_result
        utest_obj.assertTrue(apply_help_pay_result['apply_help']['apply_sorder'] == apply_sorder)
        utest_obj.assertTrue(apply_help_pay_result['apply_help']['apply_pstat'] == APYS_PAY_SUCCESS)

        ## 睡3秒，算利息
        time.sleep(3)

        accept_uid = apply_help_info['accept_uid']
        utest_obj.assertTrue(accept_uid)
        accept_token = new_access_token(accept_uid, force_passwd)

        # 接受帮助方:当前接受帮助
        cur_accept_help_result1 = cur_accept_help(MMMDAHttpRpcClt, accept_uid, accept_token)
        print "cur_accept_help_result1,", cur_accept_help_result1
        utest_obj.assertTrue('accept_help' in cur_accept_help_result1)
        utest_obj.assertTrue('apply_help_ls' in cur_accept_help_result1)
        for apply_help_dic in cur_accept_help_result1['apply_help_ls']:
            utest_obj.assertTrue('apply_piture' in apply_help_dic)
            utest_obj.assertTrue('apply_message' in apply_help_dic)

        # 接受帮助方:申请帮助确认
        acp_help_cfm_result = accept_help_confirm(MMMDAHttpRpcClt, accept_uid, accept_token, apply_sorder)
        print "acp_help_cfm_result,", acp_help_cfm_result


def get_mafuluo(id, token):
    view_account_result = account(MMMDAHttpRpcClt, id, token, id)
    print "view_account_result,", view_account_result
    assert view_account_result['result'] == error_code.ERROR_SUCCESS
    return view_account_result['account_info']['mafuluo']