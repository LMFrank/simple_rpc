# -*- coding: utf-8 -*-
from errors import InvalidOperation
from rpc_server import MethodProtocol, DivideProtocol


class ServerStub(object):
    """
    帮助服务端完成远端过程调用
    """

    def __init__(self, connection, handlers):
        """

        :param connection: 与客户端的连接
        :param handlers: 本地被调用的方法

        class Handlers:

            @staticmethod
            def divide(num1, num2=1):
                pass

            def add():
                pass
        """
        self.conn = connection
        self.method_proto = MethodProtocol(self.conn)
        self.process_map = {
            "divide": self._process_divide
        }
        self.handlers = handlers

    def process(self):
        """
        当服务端接收了一个客户端连接，建立完成后，完成远端调用处理
        :return:
        """
        # 接收消息数据，并解析方法的名字
        name = self.method_proto.get_method_name()
        # 根据解析获得的方法名，调用响应的过程协议，接收并解析消息数据
        self.process_map[name]()

    def _process_divide(self):
        """
        处理divide方法调用
        :return:
        """
        # 创建用于divide过程调用参数协议数据解析的工具
        proto = DivideProtocol()
        # 解析调用参数消息数据
        kwargs = proto.args_decode(self.conn)

        # 进行除法的本地过程调用
        # 将本地调用过程的返回值打包成消息协议数据，通过网络返回给客户端
        try:
            res = self.handlers.divide(**kwargs)
        except InvalidOperation as e:
            res_msg = proto.result_encode(e)
        else:
            res_msg = proto.result_encode(res)

        self.conn.sendall(res_msg)