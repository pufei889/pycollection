#!/usr/bin/env python
# -*- coding: utf-8 -*-
from collection import Collection
import re,sys,urllib2

class Duckgo(Collection):
    def filter(self,ttag="h2",ctag="p"):
        pas = re.compile(r"{([\s\S]*?)}",re.I|re.M)
        f = pas.findall(self.content)
        if not f: return ""
        artice = ""
        for i in f:
            print i

if __name__ == "__main__":
    a = Duckgo("https://duckduckgo.com/d.js?q=steam%20boiler&p=2")
    a.filter()
    sys.exit()
