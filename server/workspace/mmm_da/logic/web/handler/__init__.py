#!/usr/bin/python2.7
# coding=utf-8
"""
Created on 2015-4-28

@author: Jay
"""

from utils.route import route
from utils.network.http import HttpRpcHandler
from utils.wapper.web import web_adaptor
from mmm_da import setting


@route(r'/doc', name='doc')
class DocHandle(HttpRpcHandler):
    """
    根请求
    """
    @web_adaptor(use_json_dumps=False)
    def get(self):
        """
        http get 请求
        :return:
        """
        import os
        doc_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(
            os.path.realpath(__file__))))),
            'doc',
            '%s.html' % setting.SERVICE_TYPE)
        return open(doc_path).read()


@route(r'/gm_doc', name='gm_doc')
class GMDocHandle(HttpRpcHandler):
    """
    GM文档请求
    """
    @web_adaptor(use_json_dumps=False)
    def get(self):
        """
        http get 请求
        :return:
        """
        import os
        doc_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(
            os.path.realpath(__file__))))),
            'doc',
            'gm_doc.html')
        return open(doc_path).read()
