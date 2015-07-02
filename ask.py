#!/usr/bin/env python
# -*- coding: utf-8 -*-
from collection import Collection
import re,sys

class Ask(Collection):
    def filter(self,ttag="h2",ctag="p"):
        pas = re.compile(r"<div\sclass=\"web-result\sur\stsrc_tled[^>]*>([\s\S]*?)<\/div>",re.I|re.M)
        h3 = re.compile(r"<h2[^>]+>([\s\S]*?)<\/h2>",re.I|re.M)
        abstr = re.compile(r"<p[\s]class=\"web-result-description\">([\s\S]*?)<\/p>",re.I|re.M)
        f = pas.findall(self.content)
        if not f: return ""
        artice = ""
        for i in f:
            try:
                title = h3.search(i).group(1).strip() if h3.search(i) else ''
                content = abstr.search(i).group(1).strip() if abstr.search(i) else ''
                title = "<"+ttag+">"+re.sub('<[^>]+>','',title)+"</"+ttag+">\n"
                content = "<"+ctag+">"+re.sub(r'[\r\n]*','',re.sub(r'^\d+[\w\s]*...','',re.sub('<[^>]+>','',content)))+"</"+ctag+">\n"
                artice = artice + title + content
            except:
                pass
        if ( len(artice) < 5 or artice == "None"):
            return ""
        else:
            return artice

if __name__ == "__main__":
    sys.exit()
