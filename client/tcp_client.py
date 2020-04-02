# -*- coding: utf-8 -*-
import socket


class Client(object):
    """
    用于客户端建立网络连接
    """

    def __init__(self, host, port):
        """

        :param host: 服务器地址
        :param port: 服务器端口号
        """
        self.host = host
        self.port = port

    def get_connection(self):
        """
        获取连接对象
        :return: 与服务端通讯的socket
        """
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect((self.host, self.port))
        return sock