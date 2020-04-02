# -*- coding: utf-8 -*-
import unittest
from services import DivideProtocol, MethodProtocol
from io import BytesIO


class Mytest(unittest.TestCase):

    def setUp(self) -> None:
        pass

    def tearDown(self) -> None:
        pass

    def test_divide(self):
        proto = DivideProtocol()
        msg = proto.args_encode(200, 100)

        conn = BytesIO()
        conn.write(msg)
        conn.seek(0)

        # 解析消息数据
        method_proto = MethodProtocol(conn)
        name = method_proto.get_method_name()
        self.assertEqual(name, "divide")

        res = proto.args_decode(conn)
        self.assertEqual(res, {'num1': 200, 'num2': 100})


if __name__ == '__main__':
    unittest.main()
