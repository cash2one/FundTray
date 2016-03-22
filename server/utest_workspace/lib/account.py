#!/usr/bin/python2.7
# coding=utf-8
"""
Created on 2015-12-16

@author: Jay
"""
from lib.common import *
from utils.interfaces.mmm_da.http_rpc import register, login, active, add_match_coin
from utils.service_control.setting import PT_HTTPS, PT_HTTP
from utils import error_code
import random

admin0d_id = 18888
admin01_passwd = "!Admin01"

MMMDAHttpRpcClt = ServiceMgrCacher().get_connection(ST_MMM_DA, protocol=PT_HTTPS)
if not MMMDAHttpRpcClt:
    MMMDAHttpRpcClt = ServiceMgrCacher().get_connection(ST_MMM_DA, protocol=PT_HTTP)
assert MMMDAHttpRpcClt
login_result = login(MMMDAHttpRpcClt, admin0d_id, admin01_passwd)
assert login_result['result'] == error_code.ERROR_SUCCESS

admin01_access_token = login_result['access_token']
force_passwd = "!Admin01"


def new_account_id():
    return int(str(time.time()).replace('.', ''))

def new_account(can_active=True):
    new_id = new_account_id()

    register_data = {"id":new_id,
                    "passwd":force_passwd,
                    "id_card":random_str(),
                    "email":random_str(),
                    "phone":random_str(),
                    "leader_id":admin0d_id,
                    "bank":random_str(),
                    "bank_address":random_str(),
                    "bank_account":random_str(),
                    "bank_name":random_str(),
                    "wechat":random_str(),
                    "alipay":random_str()}

    # 注册
    register_result = register(MMMDAHttpRpcClt, register_data)
    assert register_result['result'] == error_code.ERROR_SUCCESS

    # 激活
    if can_active:
        active_result = active(MMMDAHttpRpcClt, admin0d_id, admin01_access_token, new_id)
        assert active_result == error_code.ERROR_SUCCESS

    # 添加拍单币
    default_match_coin = 200000
    add_match_coin_result = add_match_coin(MMMDAHttpRpcClt, admin0d_id, admin01_passwd, new_id, default_match_coin)
    return new_id, register_data['passwd']

def new_access_token(id, passwd):
    login_result = login(MMMDAHttpRpcClt, id, passwd)
    assert login_result['result'] == error_code.ERROR_SUCCESS
    return login_result['access_token']
