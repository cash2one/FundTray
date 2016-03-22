#!/usr/bin/python2.7
# coding=utf-8
"""
Created on 2015-12-30

@author: Jay
"""
MUST_KEY_SET = set(["id", "passwd",
                    "id_card", "email", "phone","leader_id",
                    "bank", "bank_address", "bank_account", "bank_name"])

OPTION_KEY_SET = set(["wechat", "alipay",
                      "create_time",
                      "login_time",
                      "active_coin", "active_time", "stat",
                      "match_coin",
                      "max_apply_money",
                      "mafuluo"])

DB_KEY_SET = set(["id"])

MEM_KEY_SET = set(["level","team_count"])

PRIVATE_KEY_SET = set(["passwd", "leader_id", "create_time", "active_coin", "active_time", "stat", "match_coin"])
PRIVATE_KEY_SET |= MEM_KEY_SET

KEY_SET = MUST_KEY_SET | OPTION_KEY_SET | DB_KEY_SET | MEM_KEY_SET

# 状态
STAT =[
    UNACTIVED,  # 未激活
    ACTIVED,    # 激活
    SEALED      # 封号
] = xrange(0, 3)

# 等级级别
LEVEL = [
    NOT_LEVEL,      # 无职位
    MGR,            # 经理
    VICE_GEN_MGR,   # 副总经理
    GEN_MGR,        # 总经理
] = xrange(0, 4)

# 等级单数需求
LEV_REQ = [
    0,
    200,
    300,
    500
]
