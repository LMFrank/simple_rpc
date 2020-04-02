# -*- coding: utf-8 -*-
from server.rpc_server import DivideProtocol


class ClientStub(object):
    """
    用来帮助客户端完成远程过程调用 RPC调用

    stub = ClinetStub()
    stub.divide(200, 100)
    """

    def __init__(self, channel):
        self.channel = channel
        self.conn = self.channel.get_connection()

    def divide(self, num1: int, num2: int = 1):
        # 将调用的参数打包成消息协议的数据
        proto = DivideProtocol()
        args = proto.args_encode(num1, num2)

        # 将消息数据通过网络发送给服务器
        self.conn.sendall(args)

        # 接收服务器返回的返回值消息数据，并进行解析
        res = proto.result_decode(self.conn)

        # 将结果返回给客户端
        if isinstance(res, float):
            return res
        else:
            raise res