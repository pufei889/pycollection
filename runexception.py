#!/usr/bin/env python
# -*- coding:utf-8 -*-

import BaseException

class RunException(BaseException):
    def __init__(self,*args):
        self.message=args[1]

    def __str__(self):
        return repr(self.message)
