#!/usr/bin/env python
# -*- coding:utf-8 -*-

class RunException(Exception):

    def __init__(self,msg):
        self.message=msg

    def __str__(self):
        return repr(self.message)
