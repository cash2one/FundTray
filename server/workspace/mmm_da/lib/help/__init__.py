#!/usr/bin/python2.7
# coding=utf-8
"""
Created on 2015-12-19

@author: Jay
"""

def apply_help_req_2_apply_help(apply_help_req):
    """
    将apply_help_req信息转成apply_help信息
    :param apply_help_req: {}
    :return: {}
    """
    if not apply_help_req:
        return {}

    return {"apply_order": apply_help_req['id'],
            "apply_stime": apply_help_req['apply_req_time'],
            "apply_money": apply_help_req['apply_req_money'],
            "apply_stat": apply_help_req['apply_req_stat']}


def accept_help_req_2_accept_help(accept_help_req):
    """
    将accept_help_req信息转成accept_help信息
    :param accept_help_req: {}
    :return: {}
    """
    if not accept_help_req:
        return {}

    return {"accept_order": accept_help_req['id'],
            "accept_stime": accept_help_req['accept_req_time'],
            "accept_money": accept_help_req['accept_req_money'],
            "accept_stat": accept_help_req['accept_req_stat']}
