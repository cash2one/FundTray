#!/usr/bin/python2.7
# coding=utf-8
"""
Created on 2015-4-28

@author: Jay
"""

"""
SYSTEM ERROR CODE
"""

ERROR_SUCCESS = 0                           # 操作成功
ERROR_UNKNOWN_ERROR = 1                     # 未知错误
ERROR_PARAMS_ERROR = 2                      # 参数格式错误
ERROR_DB_ERROR = 3                          # 数据库操作错误
ERROR_ACCESS_TOKEN_ERROR = 4                # AccessToken错误
ERROR_VERIFY_CODE_ERROR = 5                 # 验证码错误
ERROR_SIGN_ERROR = 6                        # 参数签名出错

ERROR_SERVICE_START_ERROR = 7               # 服务器启动错误

"""
LOGIC ERROR CODE
"""

ERROR_LOGIC = 440                           # 逻辑概要错误
ERROR_UID_NOT_EXIST = 441                   # uid不存在
EEROR_ACCEPT_BALANCE = 442					# 接受帮助资金平衡，请改天再来申请
EEROR_MATCH_COIN_LACK = 443                 # 排单币不足
ERROR_MAX_APPLY_HELP_LESS = 444             # 每次投资额不得低于上次投资额
ERROR_PHONE_EXISTED = 445                   # 手机号码已经存在
ERROR_PHONE_INVALID = 446                   # 手机号码无效
ERROR_ACCOUNT_SEALED = 447                  # 账号已经被封号，请联系管理员
ERROR_ACCOUNT_UNACTIVED = 448               # 账号未激活，请联系管理员
