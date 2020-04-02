# -*- coding: utf-8 -*-
import socket
import threading
from server_stub import ServerStub

class Server(object):
    """
    RPC服务器
    """

    def __init__(self, host, port, handlers):
        # 创建socket的工具对象
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        # 设置socket 重用地址
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

        # 绑定地址
        sock.bind((host, port))
        self.host = host
        self.port = port
        self.sock = sock
        self.handlers = handlers

    def serve(self):
        """
        开启服务器，提供RPC服务
        :return:
        """
        # 开启服务器的监听，等待客户端的连接请求
        self.sock.listen(128)
        print("服务器开始监听")

        # 接受客户端的连接请求
        while True:
            client_sock, client_addr = self.sock.accept()
            print(f"与客户端{str(client_addr)}建立了连接")

            # 交给ServerStub，完成客户端的具体的RPC调用请求
            stub = ServerStub(client_sock, self.handlers)
            try:
                while True:
                    stub.process()
            except EOFError:
                # 表示客户端关闭了连接
                print('客户端关闭了连接')
                client_sock.close()


class ThreadServer(object):
    """
    多线程RPC服务器
    """
    def __init__(self, host, port, handlers):
        # 创建socket的工具对象
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        # 设置socket 重用地址
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

        # 绑定地址
        sock.bind((host, port))
        self.host = host
        self.port = port
        self.sock = sock
        self.handlers = handlers

    def serve(self):
        """
        开启服务器运行，提供RPC服务
        :return:
        """
        # 开启服务器的监听，等待客户端的连接请求
        self.sock.listen(128)
        print("服务器开始监听")

        # 接受客户端的连接请求
        while True:
            client_sock, client_addr = self.sock.accept()
            print('与客户端%s建立了连接' % str(client_addr))

            # 创建子线程处理这个客户端
            t = threading.Thread(target=self.handle, args=(client_sock,))
            # 开启子线程执行
            t.start()

    def handle(self, client_sock):
        """
        子线程调用的方法，用来处理一个客户端的请求
        :return:
        """
        # 交给ServerStub，完成客户端的具体的RPC调用请求
        stub = ServerStub(client_sock, self.handlers)
        try:
            while True:
                stub.process()
        except EOFError:
            # 表示客户端关闭了连接
            print('客户端关闭了连接')
            client_sock.close()