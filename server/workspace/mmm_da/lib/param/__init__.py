#!/usr/bin/python2.7
# coding=utf-8
"""
Created on 2015-12-15

@author: Jay
"""

def is_param_equal(data, key_set):
    """
    判断是否包含所有必须参数, 并且每个参数不为0
    :param data: 数据
    :param key_set:比较的set
    :return: True/False
    """
    valid_keys = set(data.keys()) & key_set
    if valid_keys != key_set:
        return False

    for key in valid_keys:
        if len(str(data[key])) == 0:
            return False
    return True

def is_param_in(data, key_set):
    """
    判断是否包含所有许可参数, 并且每个参数不为0
    :param data: 数据
    :param key_set:比较的set
    :return: True/False
    """
    valid_keys = set(data.keys()) & key_set
    if not valid_keys:
        return False

    for key in valid_keys:
        if len(str(data[key])) == 0:
            return False
    return True

def get_valid_param(data, key_set):
    """
    获取包含所有许可参数, 并且每个参数不为0
    :param data: 数据
    :param key_set:比较的set
    :return: True/False
    """
    return dict([(key, data[key]) for key in key_set if key in data and len(str(data[key])) != 0])
