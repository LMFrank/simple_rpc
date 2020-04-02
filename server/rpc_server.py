# -*- coding: utf-8 -*-
import struct
from io import BytesIO
from errors import InvalidOperation

class Protocol(object):

    def _read_all(self, size) -> bytes:
        """
        读取二进制数据
        :param size: 需要读取的二进制数据大小
        :return: bytes 二进制数据
        """
        # self.conn
        # 读取二进制数据
        # socket.recv(4) => ?4
        # BytesIO.read
        if isinstance(self.conn, BytesIO):
            buff = self.conn.read(size)
            return buff
        else:
            # socket
            have = 0
            buff = b''
            while have < size:
                chunk = self.conn.recv(size - have)
                buff += chunk
                length = len(chunk)
                have += length

                if length == 0:
                    # 表示客户端socket关闭了
                    raise EOFError()
            return buff

class MethodProtocol(Protocol):
    """
    解读方法名
    """
    def __init__(self, connection):
        self.conn = connection

    def get_method_name(self) -> str:
        """
        提供方法名
        :return: str 方法名
        """
        # 读取字符串长度
        buff = self._read_all(4)
        length = struct.unpack("!I", buff)[0]

        # 读取字符串
        buff = self._read_all(length)
        name = buff.decode()
        return name


class DivideProtocol(Protocol):
    """
    divide过程消息协议转换工具
    """

    def args_encode(self, num1: int, num2: int = 1) -> bytes:
        """
        将原始的调用请求参数转换打包成二进制消息数据
        :param num1: int
        :param num2: int
        :return: bytes 二进制消息数据
        """
        name = "divide"
        # 处理方法名
        # 处理字符串长度
        buff = struct.pack("!I", len(name))
        # 处理字符
        buff += name.encode()

        # 处理参数1
        # 处理序号
        buff2 = struct.pack("!B", 1)
        # 处理参数值
        buff2 += struct.pack("!i", num1)

        # 处理参数2
        if num2 != 1:
            # 处理序号
            buff2 += struct.pack("!B", 2)
            # 处理参数值
            buff2 += struct.pack("!i", num2)

        # 处理消息长度，边界设定
        length = len(buff2)
        buff += struct.pack("!I", length)

        buff += buff2

        return buff

    def args_decode(self, connection) -> dict:
        """
        接收调用高清球消息数据并进行解析
        :param connection: 连接对象 socket BytesIO（测试）
        :return: dict 包含解析后的参数
        """
        param_len_map = {
            1: 4,
            2: 4
        }
        param_fmt_map = {
            1: '!i',
            2: '!i'
        }
        param_name_map = {
            1: 'num1',
            2: 'num2'
        }

        args = {}
        self.conn = connection
        # 处理方法名，已经被提前处理

        # 处理消息边界
        # 读取二进制数据
        buff = self._read_all(4)
        # 将二进制数据转换为python的数据类型
        length = struct.unpack("!I", buff)[0]

        # 已经读取的字节数
        have = 0

        # 处理第一个参数
        # 处理参数序号
        buff = self._read_all(1)
        have += 1
        param_seq = struct.unpack("!B", buff)[0]

        # 处理参数值
        param_len = param_len_map[param_seq]
        buff = self._read_all(param_len)
        have += param_len
        param_fmt = param_fmt_map[param_seq]
        param = struct.unpack(param_fmt, buff)[0]

        param_name = param_name_map[param_seq]
        args[param_name] = param

        if have >= length:
            return args

        # 处理第二个参数
        # 处理参数序号
        buff = self._read_all(1)
        param_seq = struct.unpack('!B', buff)[0]

        # 处理参数值
        param_len = param_len_map[param_seq]
        buff = self._read_all(param_len)
        param_fmt = param_fmt_map[param_seq]
        param = struct.unpack(param_fmt, buff)[0]

        param_name = param_name_map[param_seq]
        args[param_name] = param

        return args

    def result_encode(self, result) -> bytes:
        """
        将原始结果数据转换为消息协议二进制数据
        :param result: float 原始结果数据 or InvalidOperation
        :return: bytes 消息协议二进制数据
        """
        # 正常
        if isinstance(result, float):
            pass
            # 处理返回值类型
            buff = struct.pack("!B", 1)
            buff += struct.pack("!f", result)
            return buff
        # 异常
        else:
            # 处理返回值类型
            buff = struct.pack("!B", 2)
            # 处理返回值
            length = len(result.message)
            # 处理字符串长度
            buff += struct.pack("!I", length)
            # 处理字符
            buff += result.message.encode()
            return buff

    def result_decode(self, connection):
        """
        将返回值消息数据转换为原始返回值
        :param connection: socket BytesIO
        :return: float or InvalidOperation
        """
        self.conn = connection

        # 处理返回值类型
        buff = self._read_all(1)
        res_type = struct.unpack("!B", buff)[0]
        if res_type == 1:
            # 读取float数据
            buff = self._read_all(4)
            val = struct.unpack("!f", buff)[0]
            return val
        else:
            # 读取字符串长度
            buff = self._read_all(4)
            length = struct.unpack("!I", buff)[0]
            # 读取字符串
            buff = self._read_all(length)
            msg = buff.decode()
            return InvalidOperation(msg)
