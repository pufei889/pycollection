#!/usr/bin/env python
# -*- coding: utf-8 -*-
from collection import Collection
import re,sys
class Gmx(Collection):
    def filter(self,ttag="h2",ctag="p"):
        main = re.compile(r"<div\sclass=\"searchResults\"[^>]*>([\s\S]*?)<\/div>")
        pas = re.compile(r"<li[^>]*>([\s\S]*?)<\/li>",re.I|re.M)
        h3 = re.compile(r"<h3>([\s\S]*?)<\/h3>",re.I|re.M)
        abstr = re.compile(r"<p>([\s\S]*?)<\/p>",re.I|re.M)
        c = main.search(self.content)
        if not c: return ""
        f = pas.findall(c.group(1))
        artice = ""
        for i in f:
            try:
                title = h3.search(i).group(1).strip() if h3.search(i) else ''
                content = abstr.search(i).group(1).strip() if abstr.search(i) else ''
                title = "<"+ttag+">"+re.sub(r'<[^>]+>','',title)+"</"+ttag+">\n"
                content = "<"+ctag+">"+re.sub(r'<[^>]+>','',content)+"</"+ctag+">\n"
                artice = artice + title + content
            except:
                pass
        if ( len(artice) < 5 or artice == "None"):
            return ""
        else:
            return artice

if __name__ == "__main__":
    sys.exit()
