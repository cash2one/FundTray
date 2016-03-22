#!/usr/bin/python2.7
# coding=utf-8
"""
Created on 2015-7-25

@author: Jay
"""
from gevent import monkey
monkey.patch_all()
from utils import logger
import collections
from geventwebsocket import WebSocketServer, WebSocketApplication, Resource
import tornado
import tornado.escape
from utils.wapper.catch import except_adaptor
from utils.service_control.setting import PT_WEB_SOCKET
from utils.network.tcp import TcpRpcServer


class WSRpcApplication(WebSocketApplication):
    waiters = set()
    handlers = {}
    def get_compression_options(self):
        # Non-None enables compression with default options.
        return {}

    def on_open(self):
        logger.info("WSRpcApplication::on_open,%s" % self)
        WSRpcApplication.waiters.add(self)

    def on_close(self):
        logger.info("WSRpcApplication::on_close,%s" % self)
        WSRpcApplication.waiters.remove(self)

    @classmethod
    def send_message(cls, message):
        logger.info("WSRpcApplication::send_message, message:%s, %s" % (message, cls))
        for waiter in cls.waiters:
            try:
                waiter.ws.send(message)
            except:
                logger.error("WSRpcApplication::send_message Error", exc_info=True)

    @except_adaptor()
    def on_message(self, message):
        if not message:
            logger.error("WSRpcApplication::on_message, message is None!!!")
            return

        logger.info("WSRpcApplication::on_message, message:%s, %s" % (message, self))
        message = tornado.escape.json_decode(message)
        assert "type" in message
        if message['type'] not in self.handlers:
            error_msg = "WSRpcApplication::on_message, subject:%s not register, details:%s" % (message['type'], self.handlers)
            logger.error(error_msg)
            return

        self.handlers[message['type']](message)

    @classmethod
    def reg_message(cls, subject, hander_fun):
        cls.handlers[subject] = hander_fun


class WsRpcServer(TcpRpcServer):
    waiters = set()
    handlers = {}

    def __init__(self, ssl_args, port, application=WSRpcApplication):
        self.port = port
        self.application = application
        patterns = {'/websocket': application}
        res = Resource(collections.OrderedDict(sorted(patterns.items(), key=lambda t: t[0])))
        self.server = WebSocketServer(('', port), res, **ssl_args)
        self.protocol = PT_WEB_SOCKET
