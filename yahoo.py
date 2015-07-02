#!/usr/bin/env python
# -*- coding=utf-8 -*-
from collection import Collection
import re,sys
class Yahoo(Collection):
    def filter(self,ttag="h2",ctag="p"):
        pas = re.compile(r"<div class=\"dd algo[^>]*>([\s\S]*?)<\/div><\/li>",re.I|re.M)
        h3 = re.compile(r"<h3[^>]*>([\s\S]*?)<\/h3>",re.I|re.M)
        abstr = re.compile(r"<div\sclass=\"compText aAbs\"[^>]*>([\s\S]*?)<\/div>",re.I|re.M)
        f = pas.findall(self.content)
        if not f: return ""
        artice = ""
        for i in f:
            try:
                title = h3.search(i).group(1) if h3.search(i) else ''
                content = abstr.search(i).group(1) if abstr.search(i) else ''
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
