#!/usr/bin/python2.7
# coding=utf-8
"""
Created on 2015-7-25

@author: Jay
"""
from gevent import monkey
monkey.patch_all()
from tornado.web import RequestHandler
from tornado.wsgi import WSGIApplication
from gevent.wsgi import WSGIServer
import urllib2
from tornado.web import url
from utils.wapper.web import web_adaptor
from utils.wapper.stackless import gevent_adaptor
from utils import logger
from utils.service_control.setting import PT_HTTP, PT_HTTPS
from utils.network import PING_RESPONSE
from utils.network.tcp import TcpRpcServer, TcpRpcClient


class HttpRpcHandler(RequestHandler):
    """
    HttpRpc回调处理类
    """
    _sessions_ = {}

    def render_string(self, template_name, **context):
        """
        字符串渲染
        :param template_name:
        :param context:
        :return:
        """
        if self.application.jinja_env:
            template = self.application.jinja_env.get_template(template_name,
                                                               parent=self.get_template_path())
            context['auto_reload'] = False
            return template.render(**context)
        else:
            RequestHandler.render_string(self, template_name, **context)

    def get(self, *args, **kwargs):
        """
        http get 请求
        :param args:
        :param kwargs:
        :return:
        """
        return self.post(*args, **kwargs)

    def post(self, *args, **kwargs):
        """
        http post 请求
        :param args:
        :param kwargs:
        :return:
        """
        return self.get(*args, **kwargs)

    @web_adaptor()
    def options(self, *args, **kwargs):
        self.set_header('Access-Control-Allow-Origin', '*')
        self.set_header('Access-Control-Allow-Methods', 'GET, POST, DELETE')
        self.set_header('Access-Control-Allow-Headers', 'Accept, Content-Type, Authorization, ID')
        return

    def get_request_ip(self):
        """
        获取请求ip
        :return:
        """
        return self.request.remote_ip

    def reponse_msg(self, msg, url=None):
        """
        url消息提示跳转
        :param msg: 需要提示的消息
        :param url: 跳转的url
        :return: None
        """
        msg_dic = {"msg":msg}
        if url:
            msg_dic["url"] = url
        self.render("auto_refresh.html", **msg_dic)

    def get_current_user(self):
        return self.get_secure_cookie('username',None)




class HttpPingHandle(HttpRpcHandler):
    """
    http ping 处理器
    """
    @web_adaptor(use_json_dumps=False)
    def get(self):
        """
        Http get 请求
        """
        return PING_RESPONSE

    def post(self):
        """
        http post 请求
        """
        return self.get()


class SetLoggerLevelHandle(HttpRpcHandler):
    """
    设置日志等级
    """

    @web_adaptor(use_json_dumps=False)
    def get(self, logger_level):
        """
        Http get 请求
        """
        logger.set_logger_level(logger_level)
        return {"result": 0}

    def post(self, *args, **kwargs):
        """
        http post 请求
        """
        return self.get(*args, **kwargs)


class HttpRpcServer(TcpRpcServer, WSGIApplication):
    """
    HttpRpc服务器
    """

    def __init__(self, ssl_args, port, handlers=None, default_host="", jinja_env=None, **settings):
        handlers += [url("/ping", HttpPingHandle, {}, "ping handler")]
        handlers += [url("/set_logger_level", SetLoggerLevelHandle, {}, "Set Logger Level handler")]
        WSGIApplication.__init__(self, handlers, default_host, **settings)
        self.server = WSGIServer(('', port), self, **ssl_args)
        self.port = port
        self.protocol = PT_HTTPS if ssl_args else PT_HTTP
        self.jinja_env = jinja_env


class HttpRpcClient(TcpRpcClient):
    """
    HttpRpc客户端
    """

    def __init__(self, host=None, port=None, ssl=False):
        self.host, self.port = host, port
        self.ssl = ssl

    def __get_full_url(self, url):
        """
        获取完整的可访问的url
        :param url: url链接，有可能只是接口
        :return:
        """
        protocol = "https" if self.ssl else "http"
        return '%s://%s:%s/%s' % (protocol, self.host, self.port, url) \
            if self.host and self.port \
            else url

    def _rpc_fetch(self, url, headers={}, body=None, method=None):
        """
        rpc函数调用实现
        :param url: url
        :param headers: headers
        :param body: body
        :param method: mothod
        :return:
        """
        full_url = self.__get_full_url(url)
        req = urllib2.Request(full_url, body, headers)
        if method:
            req.get_method = lambda:method

        try:
            result = urllib2.urlopen(req).read()
        except Exception, e:
            logger.error("HttpRpcClient::_rpc_fetch failed, url:%s headers:%s body:%s msg:%s" % (full_url, headers, body, e.message))
            raise
        if isinstance(result, Exception):
            raise result
        return result

    @gevent_adaptor()
    def fetch_async(self, url, headers={}, body=None, method=None):
        """
        协程非阻塞调用
        :param url: url
        :param headers: headers
        :param body:  body
        :param method:  mothod
        :return:
        """
        return self._rpc_fetch(url, headers, body, method)

    def fetch_sync(self, url, headers={}, body=None, method=None):
        """
        阻塞调用
        :param url: url
        :param headers: headers
        :param body:  body
        :param method:  mothod
        :return:
        """
        return self._rpc_fetch(url, headers, body, method)

    def ping(self):
        """
        ping 函数调用
        :return:
        """
        return self.fetch_sync("ping")
