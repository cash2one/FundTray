#!/usr/bin/python2.7
# coding=utf-8
"""
Created on 2016-2-20

@author: Jay
"""

def daysdiff(d1, d2):
    """
    计算两个时间戳的天数差距
    :param d1: 时间戳
    :param d2: 时间戳
    :return:
    """
    from mmm_da.lib.server_info import ServerInfoMgr
    return float((d1 - d2)/ServerInfoMgr().attr_day_seconds)

def hoursdiff(d1, d2):
    """
    计算两个时间戳的小时数差距
    :param d1: 时间戳
    :param d2: 时间戳
    :return:
    """
    from mmm_da.lib.server_info import ServerInfoMgr
    hour_seconds = ServerInfoMgr().attr_day_seconds/float(24)
    return float((d1 - d2)/hour_seconds)


def calc_pi(principal, interest, stime, etime):
    """
    计算本息
    :param principal: 本金
    :param interest: 利息
    :param stime: 开始时间
    :param etime: 结束时间
    :return: 所得本息
    """
    int_days = daysdiff(etime, stime)
    pi = principal * (1 + float(interest) / 100 * int_days)
    return int(pi)

def calc_match_coin(apply_money):
    """
    计算排单币
    :param apply_money: 申请帮助的金额
    :return:
    """
    from mmm_da.lib.server_info import ServerInfoMgr
    return apply_money * ServerInfoMgr().attr_match_coin_loss / 100
