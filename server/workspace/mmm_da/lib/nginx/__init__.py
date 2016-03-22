#!/usr/bin/python2.7
# coding=utf-8
"""
Created on 2015-12-19

@author: Jay
"""
import os
from utils import logger
import platform
from gevent import subprocess
from utils.service_control.parser import ArgumentParser


def mv_pay_pic(src_file_path, tgt_file_name, tgt_file_path):
    """
    移动支付截图文件，从存储的地方移动到下载地方
    :param src_file_path: 源文件路径
    :param tgt_file_name: 目的文件名称
    :param tgt_file_path: 目的文件路径
    :return:
    """
    if not os.path.exists(tgt_file_path):
            os.makedirs(tgt_file_path)

    tgt_path = "%s/%s" % (tgt_file_path, tgt_file_name)
    if platform.system() == 'Linux':
        mv_cmd = "sudo mv %s %s" % (src_file_path, tgt_path)

        # 如果图片存储主机不是本机，则需要ssh远程连接，同时需要能实现ssh无密码登录
        if ArgumentParser().args.pic_store_ip != "localhost":
            mv_cmd = "ssh -p%s %s@%s %s" % (ArgumentParser().args.pic_store_port,
                                            ArgumentParser().args.pic_store_user,
                                            ArgumentParser().args.pic_store_ip,
                                            mv_cmd)

        subprocess.Popen(mv_cmd, shell=True)
        logger.info("mv_pay_pic src_file_path:%s tgt_path:%s, mv_cmd:%s" % (src_file_path, tgt_path, mv_cmd))


def rm_pay_pic(tgt_file_path):
    """
    删除支付截图文件，
    :param tgt_file_path: 目的文件路径
    :return:
    """
    if not os.path.exists(tgt_file_path):
            os.makedirs(tgt_file_path)

    if platform.system() == 'Linux':
        rm_cmd = "sudo rm %s" % tgt_file_path

        # 如果图片存储主机不是本机，则需要ssh远程连接，同时需要能实现ssh无密码登录
        if ArgumentParser().args.pic_store_ip != "localhost":
            rm_cmd = "ssh -p%s %s@%s %s" % (ArgumentParser().args.pic_store_port,
                                            ArgumentParser().args.pic_store_user,
                                            ArgumentParser().args.pic_store_ip,
                                            rm_cmd)

        subprocess.Popen(rm_cmd, shell=True)
        logger.info("rm_pay_pic tgt_file_path:%s, rm_cmd:%s" % (tgt_file_path, rm_cmd))