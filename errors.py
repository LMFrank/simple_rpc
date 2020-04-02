# -*- coding: utf-8 -*-
class InvalidOperation(Exception):

    def __init__(self, message=None):
        self.message = message or "Invalid operation"