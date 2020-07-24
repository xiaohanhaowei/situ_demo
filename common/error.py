# -*- coding: utf-8 -*-

class MyError(Exception):
    def __init__(self,code,msg):
        self.code = code
        self.msg = msg

    def __str__(self):
        return self.msg

