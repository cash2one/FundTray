#!/usr/bin/python2.7
# coding=utf-8
"""
Created on 2015-7-25

@author: Jay
"""
from gevent import monkey
monkey.patch_all()
from gevent.server import DatagramServer
from utils.wapper.stackless import gevent_adaptor
from gevent import socket
from utils.service_control.setting import PT_UDP
from utils.network.tcp import TcpRpcServer


class UdpServer(TcpRpcServer):
    def __init__(self, port):
        self.port = port
        self.server = DatagramServer(('', self.port), handle=self.handle)
        self.protocol = PT_UDP

    def handle(self, data, address):
        self.server.sendto(data, address)


class UdpClient(object):
    def __init__(self, host, port):
        self.server_addr = (host, port)
        self.socket = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)

    def _send(self, data):
        self.socket.sendto(data, self.server_addr)

    @gevent_adaptor()
    def send_async(self, data):
        self._send(data)

    def send_sync(self, data):
        self._send(data)