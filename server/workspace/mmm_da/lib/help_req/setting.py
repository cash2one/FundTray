#!/usr/bin/python2.7
# coding=utf-8
"""
Created on 2015-12-21

@author: Jay
"""
APPLY_REQ_STAT = [
    APYRS_REQUEST,         # 提供帮助请求提交(对于客户端来说，也是处理匹配状态)
    APYRS_FINISH,          # 提供帮助请求完成
] = xrange(10, 12)

ACCEPT_REQ_STAT = [
    ACPRS_REQUEST,         # 接收帮助请求提交(对于客户端来说，也是处理匹配状态)
    ACPRS_FINISH,          # 接收帮助请求完成
] = xrange(10, 12)


MIN_APPLY_HELP_MONEY = 1000
MAX_APPLY_HELP_MONEY = 20000