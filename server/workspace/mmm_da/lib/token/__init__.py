#!/usr/bin/python2.7
# coding=utf-8
"""
Created on 2015-12-15

@author: Jay
"""
from utils.crypto.xxtea import XXTEA
import base64
from utils import error_code

xxtea_obj = XXTEA("acdfvgb123456789")

class TokenMgr(object):
    """
    访问码管理器
    """

    @staticmethod
    def generate_access_token(id):
        """
        根据用户名，产生新的访问token，并保持相关的访问key到数据访问层
        :param id: 用户id
        :return:字符串
        """
        s = xxtea_obj.encrypt(str(id))
        s = base64.b64encode(s)
        return s

    @staticmethod
    def check_expire_access_token(access_token, id):
        """
        检查access token是否合法
        :param access_token:
        :param phone: 手机号
        :return:
        """
        s = base64.b64decode(access_token)
        s = xxtea_obj.decrypt(s)
        return str(s) == str(id)