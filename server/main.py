# -*- coding: utf-8 -*-
from errors import InvalidOperation
from tcp_server import Server, ThreadServer


class Handlers(object):

    @staticmethod
    def divide(num1: int, num2: int = 1):
        """
        除法
        :param num1: int
        :param num2: int
        :return: float
        """
        if num2 == 0:
            raise InvalidOperation()
        val = num1 / num2
        return val


if __name__ == '__main__':
    # 开启服务器
    # _server = Server("127.0.0.1", 8000, Handlers)
    _server = ThreadServer("127.0.0.1", 8000, Handlers)
    _server.serve()