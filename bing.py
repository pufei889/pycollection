#!/usr/bin/env python
# -*- coding: utf-8 -*-
from collection import Collection
import re,sys

class Bing(Collection):
        def filter(self,ttag="h2",ctag="p"):
                if not self.content : return
                
                pas = re.compile(r"<li class=\"b_algo[^>]*>([\s\S]*?)<\/div><\/li>",re.I|re.M)
                h3 = re.compile(r"<h2[^>]*>([\s\S]*?)<\/h2>",re.I|re.M)
                abstr = re.compile(r"<p>([\s\S]*?)<\/p>",re.I|re.M)
                f = pas.findall(self.content)
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
