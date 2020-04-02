# -*- coding: utf-8 -*-
from errors import InvalidOperation


def divide(num1: int, num2: int = 1):
    """
    除法
    :param num1: int
    :param num2: int
    :return: float
    """
    if num2 == 0:
        raise InvalidOperation
    val = num1 / num2
    return val

try:
    res = divide(200, 100)
except InvalidOperation as e:
    print(e.message)
else:
    print(res)