#!/usr/bin/python2.7
# coding=utf-8
"""
Created on 2015-12-19

@author: Jay
"""

APPLY_STAT =[
    APYS_MATCHING,        # 匹配中
    APYS_FINISH,          # 订单完成：已经提取
    APYS_UNUSUAL,         # 订单异常
] = xrange(0, 3)

ACCEPT_STAT=[
    ACPS_MATCHING,        # 匹配中
    ACPS_FINISH,          # 完成
] = xrange(0, 2)
