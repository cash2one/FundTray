#!/usr/bin/python2.7
# coding=utf-8
"""
Created on 2016-2-24

@author: Jay
"""

APPLY_PAY_STAT =[
    APYS_PAY_WAIT,      # 等待支付
    APYS_PAY_SUCCESS,   # 支付成功
    APYS_PAY_CFRM,      # 确认支付
    APYS_PAY_UNUSUAL,   # 支付异常
    APYS_PAY_REFUSE,    # 拒绝支付
    APYS_PAY_FINISH,    # 支付完成
] = xrange(0, 6)

