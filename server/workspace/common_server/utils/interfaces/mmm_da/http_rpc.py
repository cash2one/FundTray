#!/usr/bin/python2.7
# coding=utf-8
"""
Created on 2015-7-23

@author: Jay
"""
import urllib
import ujson


def register(http_rpc_client, register_dict):
    body = urllib.quote(ujson.dumps(register_dict))
    url = "register"
    return ujson.loads(urllib.unquote(http_rpc_client.fetch_async(url, body=body)))


def login(http_rpc_client, id, passwd):
    body = {'id': id, "passwd": passwd}
    body = urllib.quote(ujson.dumps(body))
    url = "login"
    return ujson.loads(urllib.unquote(http_rpc_client.fetch_async(url, body=body)))


def account(http_rpc_client, id, access_token, id2, account_dict={}, headers={}, body=None):
    headers = {'Authorization': access_token,
               'id': id}

    body = urllib.quote(ujson.dumps(account_dict)) if account_dict else None

    url = "account/%s" % id2

    if body:
        headers['Content-Type']= 'text/plain;charset=UTF-8'
    return ujson.loads(urllib.unquote(http_rpc_client.fetch_async(url, headers, body)))

def passwd_change(http_rpc_client, id, access_token, old_passwd, new_passwd):
    headers = {'Authorization': access_token,
               'id': id}

    body = {"old_passwd": old_passwd, "new_passwd": new_passwd}
    body = urllib.quote(ujson.dumps(body))

    url = "passwd_change"

    if body:
        headers['Content-Type']= 'text/plain;charset=UTF-8'
    return ujson.loads(urllib.unquote(http_rpc_client.fetch_async(url, headers, body)))


def add_active_coin(http_rpc_client, id, passwd, adding_id, adding_coin):
    url = "add_active_coin/%s/%s/%s/%s" % (id, passwd, adding_id, adding_coin)
    return ujson.loads(urllib.unquote(http_rpc_client.fetch_async(url)))

def active(http_rpc_client, id, access_token, active_id):
    headers = {'Authorization': access_token,
               'id': id}

    url = "active/%s" % active_id
    return ujson.loads(urllib.unquote(http_rpc_client.fetch_async(url, headers)))


def summary(http_rpc_client, id, access_token):
    headers = {'Authorization': access_token,
               'id': id}

    url = "summary"
    return ujson.loads(urllib.unquote(http_rpc_client.fetch_async(url, headers)))

def server_setting(http_rpc_client, id, passwd, field, value):
    url = "server_setting/%s/%s/%s/%s" % (id, passwd, field, value)
    return ujson.loads(urllib.unquote(http_rpc_client.fetch_async(url)))

def seal_account(http_rpc_client, id, passwd, seal_id):
    url = "seal_account/%s/%s/%s" % (id, passwd, seal_id)
    return ujson.loads(urllib.unquote(http_rpc_client.fetch_async(url)))

def unseal_account(http_rpc_client, id, passwd, seal_id):
    url = "unseal_account/%s/%s/%s" % (id, passwd, seal_id)
    return ujson.loads(urllib.unquote(http_rpc_client.fetch_async(url)))

def apply_help(http_rpc_client, id, access_token, apply_money):
    """
    申请帮助
    :param http_rpc_client:
    :param id:  id
    :param access_token: token
    :param apply_money: 申请帮助金额
    :return:
    """
    headers = {'Authorization': access_token,
               'id': id}

    body = {"apply_money": apply_money}
    body = urllib.quote(ujson.dumps(body))

    url = "apply_help"

    if body:
        headers['Content-Type']= 'text/plain;charset=UTF-8'
    return ujson.loads(urllib.unquote(http_rpc_client.fetch_async(url, headers, body)))

def del_apply_help(http_rpc_client, id, access_token, apply_order):
    """
    申请帮助删除
    :param http_rpc_client:
    :param id:  id
    :param access_token: token
    :param apply_order: 申请帮助订单
    :return:
    """
    headers = {'Authorization': access_token,
               'id': id}

    body = {"apply_order": apply_order}
    body = urllib.quote(ujson.dumps(body))

    url = "del_apply_help"

    if body:
        headers['Content-Type']= 'text/plain;charset=UTF-8'
    return ujson.loads(urllib.unquote(http_rpc_client.fetch_async(url, headers, body)))

def cur_apply_help(http_rpc_client, id, access_token):
    """
    当前申请帮助列表
    :param http_rpc_client:
    :param id:  id
    :param access_token: token
    :return:
    """
    headers = {'Authorization': access_token,
               'id': id}

    url = "cur_apply_help"
    return ujson.loads(urllib.unquote(http_rpc_client.fetch_async(url, headers)))

def apply_help_paid(http_rpc_client, id, access_token, apply_sorder, pay_msg, file_path, file_name):
    """
    申请帮助支付
    :param http_rpc_client:
    :param id: id
    :param access_token: token
    :param apply_sorder: 申请帮助子id
    :param pay_piture:  支付截图
    :param pay_msg:  支付消息
    :return:
    """
    body = {"id": id,
            "access_token": access_token,
            "apply_sorder": apply_sorder,
            "pay_msg": pay_msg,
            "file_path": file_path,
            "file_name": file_name}
    body = "&".join("%s=%s" % (urllib.quote(k), urllib.quote(str(v))) for k, v in body.items())

    url = "apply_help_paid?%s" % body
    return ujson.loads(urllib.unquote(http_rpc_client.fetch_async(url, body=body)))

def apply_help_refuse(http_rpc_client, id, access_token, apply_sorder):
    """
    拒绝支付申请帮助订单
    :param http_rpc_client:
    :param id:  id
    :param access_token: token
    :param apply_sorder: 申请支付子订单id
    :return:
    """
    headers = {'Authorization': access_token,
               'id': id}

    body = {"apply_sorder": apply_sorder}
    body = urllib.quote(ujson.dumps(body))

    url = "apply_help_refuse"

    if body:
        headers['Content-Type']= 'text/plain;charset=UTF-8'
    return ujson.loads(urllib.unquote(http_rpc_client.fetch_async(url, headers, body)))


def accept_help(http_rpc_client, id, access_token, mafuluo):
    """
    接受帮助申请
    :param http_rpc_client:
    :param id: id
    :param access_token: token
    :param mafuluo: 接受帮助马夫罗
    :return:
    """
    headers = {'Authorization': access_token,
               'id': id}

    body = {"mafuluo": mafuluo}
    body = urllib.quote(ujson.dumps(body))

    url = "accept_help"

    if body:
        headers['Content-Type']= 'text/plain;charset=UTF-8'
    return ujson.loads(urllib.unquote(http_rpc_client.fetch_async(url, headers, body)))

def del_accept_help(http_rpc_client, id, access_token, accept_order):
    """
    接受帮助删除
    :param http_rpc_client:
    :param id:  id
    :param access_token: token
    :param accept_order: 申请帮助订单
    :return:
    """
    headers = {'Authorization': access_token,
               'id': id}

    body = {"accept_order": accept_order}
    body = urllib.quote(ujson.dumps(body))

    url = "del_accept_help"

    if body:
        headers['Content-Type']= 'text/plain;charset=UTF-8'
    return ujson.loads(urllib.unquote(http_rpc_client.fetch_async(url, headers, body)))

def cur_accept_help(http_rpc_client, id, access_token):
    """
    获取当前接受帮助列表
    :param http_rpc_client:
    :param id: id
    :param access_token: token
    :return:
    """
    headers = {'Authorization': access_token,
               'id': id}

    url = "cur_accept_help"
    return ujson.loads(urllib.unquote(http_rpc_client.fetch_async(url, headers)))


def accept_help_confirm(http_rpc_client, id, access_token, apply_sorder):
    """
    接受帮助确认
    :param http_rpc_client:
    :param id: id
    :param access_token: token
    :param apply_sorder: 申请帮助子订单
    :return:
    """
    headers = {'Authorization': access_token,
               'id': id}

    body = {"apply_sorder": apply_sorder}
    body = urllib.quote(ujson.dumps(body))

    url = "accept_help_confirm"

    if body:
        headers['Content-Type']= 'text/plain;charset=UTF-8'
    return ujson.loads(urllib.unquote(http_rpc_client.fetch_async(url, headers, body)))


def accept_help_notreceived(http_rpc_client, id, access_token, apply_sorder):
    """
    接受帮助未收到
    :param http_rpc_client:
    :param id: id
    :param access_token: token
    :param apply_sorder: 申请帮助子订单
    :return:
    """
    headers = {'Authorization': access_token,
               'id': id}

    body = {"apply_sorder": apply_sorder}
    body = urllib.quote(ujson.dumps(body))

    url = "accept_help_notreceived"

    if body:
        headers['Content-Type']= 'text/plain;charset=UTF-8'
    return ujson.loads(urllib.unquote(http_rpc_client.fetch_async(url, headers, body)))


def random_leader_id(http_rpc_client):
    url = "random_leader_id"
    return ujson.loads(urllib.unquote(http_rpc_client.fetch_async(url)))

def system_info(http_rpc_client,id, access_token):
    """
    获取系统信息
    :param http_rpc_client:
    :param id: id
    :param access_token: token
    """
    headers = {'Authorization': access_token,
                'id': id}
    url = "system_info"
    return ujson.loads(urllib.unquote(http_rpc_client.fetch_async(url, headers)))

def set_notice(http_rpc_client, id, passwd, notice):
    url = "set_notice/%s/%s/%s" % (id, passwd, notice)
    return ujson.loads(urllib.unquote(http_rpc_client.fetch_async(url)))


def get_history_notice(http_rpc_client, id, passwd):
    url = "get_history_notice/%s/%s" % (id, passwd)
    return ujson.loads(urllib.unquote(http_rpc_client.fetch_async(url)))


def add_accept_help(http_rpc_client, id, passwd, req_id, req_money):
    url = "add_accept_help/%s/%s/%s/%s" % (id, passwd, req_id, req_money)
    return ujson.loads(urllib.unquote(http_rpc_client.fetch_async(url)))

def add_apply_help(http_rpc_client, id, passwd, req_id, req_money):
    url = "add_apply_help/%s/%s/%s/%s" % (id, passwd, req_id, req_money)
    return ujson.loads(urllib.unquote(http_rpc_client.fetch_async(url)))

def check_id(http_rpc_client, id):
    body = {"id": id}
    body = urllib.quote(ujson.dumps(body))

    url = "check_id"
    return urllib.unquote(http_rpc_client.fetch_async(url, body=body))

def add_match_coin(http_rpc_client, id, passwd, adding_id, adding_coin):
    url = "add_match_coin/%s/%s/%s/%s" % (id, passwd, adding_id, adding_coin)
    return ujson.loads(urllib.unquote(http_rpc_client.fetch_async(url)))

def auto_match(http_rpc_client, id, passwd, apply_uid, accept_uid, apply_money):
    url = "auto_match/%s/%s/%s/%s/%s" % (id, passwd, apply_uid, accept_uid, apply_money)
    return ujson.loads(urllib.unquote(http_rpc_client.fetch_async(url)))


def get_bonus_logs(http_rpc_client,id, access_token, page_idx=1):
    """
    获取系统奖金日志
    :param http_rpc_client:
    :param id: id
    :param access_token: token
    """
    headers = {'Authorization': access_token,
                'id': id}

    body = {"page_idx": page_idx}
    body = urllib.quote(ujson.dumps(body))

    url = "get_bonus_logs"
    return ujson.loads(urllib.unquote(http_rpc_client.fetch_async(url, headers, body)))

def check_phone(http_rpc_client, phone):
    body = {"phone": phone}
    body = urllib.quote(ujson.dumps(body))

    url = "check_phone"
    return urllib.unquote(http_rpc_client.fetch_async(url, body=body))

def active_coin_transfer(http_rpc_client,id, access_token, tgt_id, tgt_coin):
    """
    激活币转账
    :param http_rpc_client:
    :param id: id
    :param access_token: token
    """
    headers = {'Authorization': access_token,
                'id': id}

    body = {"tgt_id": tgt_id,
            "tgt_coin": tgt_coin}
    body = urllib.quote(ujson.dumps(body))

    url = "active_coin_transfer"
    return ujson.loads(urllib.unquote(http_rpc_client.fetch_async(url, headers, body)))

def match_coin_transfer(http_rpc_client,id, access_token, tgt_id, tgt_coin):
    """
    配单币转账
    :param http_rpc_client:
    :param id: id
    :param access_token: token
    """
    headers = {'Authorization': access_token,
                'id': id}

    body = {"tgt_id": tgt_id,
            "tgt_coin": tgt_coin}
    body = urllib.quote(ujson.dumps(body))

    url = "match_coin_transfer"
    return ujson.loads(urllib.unquote(http_rpc_client.fetch_async(url, headers, body)))

def apply_help_list(http_rpc_client, id, access_token):
    """
    申请帮助列表
    :param http_rpc_client:
    :param id: id
    :param access_token: token
    :return:
    """
    headers = {'Authorization': access_token,
               'id': id}

    url = "apply_help_list"
    return ujson.loads(urllib.unquote(http_rpc_client.fetch_async(url, headers)))

def accept_help_list(http_rpc_client, id, access_token):
    """
    接受帮助列表
    :param http_rpc_client:
    :param id: id
    :param access_token: token
    :return:
    """
    headers = {'Authorization': access_token,
               'id': id}

    url = "accept_help_list"
    return ujson.loads(urllib.unquote(http_rpc_client.fetch_async(url, headers)))


def gm_login(http_rpc_client, id, passwd):
    body = {'id': id, "passwd": passwd}
    body = urllib.quote(ujson.dumps(body))
    url = "gm_login"
    return ujson.loads(urllib.unquote(http_rpc_client.fetch_async(url, body=body)))

def view_account(http_rpc_client, id, passwd, view_uid):
    url = "view_account/%s/%s/%s" % (id, passwd, view_uid)
    return ujson.loads(urllib.unquote(http_rpc_client.fetch_async(url)))

def active_account(http_rpc_client, id, passwd, active_uid):
    url = "active_account/%s/%s/%s" % (id, passwd, active_uid)
    return ujson.loads(urllib.unquote(http_rpc_client.fetch_async(url)))

def all_server_setting(http_rpc_client, id, access_token):
    headers = {'Authorization': access_token,
               'id': id}

    url = "all_server_setting"
    return ujson.loads(urllib.unquote(http_rpc_client.fetch_async(url, headers)))

def reset_server_setting(http_rpc_client, id, access_token, upd_setting_dic):
    headers = {'Authorization': access_token,
               'id': id}
    body = urllib.quote(ujson.dumps(upd_setting_dic))
    url = "reset_server_setting"
    return ujson.loads(urllib.unquote(http_rpc_client.fetch_async(url, headers, body)))

def login_info(http_rpc_client, id, passwd, last_minutes):
    url = "login_info/%s/%s/%s" % (id, passwd, last_minutes)
    return ujson.loads(urllib.unquote(http_rpc_client.fetch_async(url)))