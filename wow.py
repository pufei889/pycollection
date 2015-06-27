#!/usr/bin/env python
# -*- coding: utf-8 -*-
from collection import Collection
import re,sys

class Wow(Collection):
    def filter(self,ttag="h2",ctag="p"):
        if not self.content:return

        pas = re.compile(r"<li about=\"null\">([\s\S]*?)<\/li>",re.I|re.M)
        h3 = re.compile(r"<a[^>]*>([\s\S]*?)<\/a>",re.I|re.M)
        abstr = re.compile(r"<p property=\"f:desc\">([\s\S]*?)<\/p>",re.I|re.M)
        f = pas.findall(self.content)
        artice = ""
        for i in f:
            try:
                title = h3.search(i).group(1).strip()
                content = abstr.search(i).group(1).strip()
                title = "<"+ttag+">"+re.sub(r'<[^>]+>','',title)+"</"+ttag+">\n"
                content = "<"+ctag+">"+re.sub(r'[\r\n]*','',re.sub(r'^\d+[\w\s]*...','',re.sub(r'<[^>]+>','',content)))+"</"+ctag+">\n"
                artice = artice + title + content
            except:
                pass
        if ( len(artice) < 5 or artice == "None"):
            return ""
        else:
            return artice
                        
if __name__ == "__main__":
    sys.exit()
