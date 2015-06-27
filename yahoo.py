#!/usr/bin/env python
# -*- coding=utf-8 -*-
from collection import Collection
import re
class Yahoo(Collection):
        
        def filter(self,ttag="h2",ctag="p"):
                if not self.content : return
                
                pas = re.compile(r"<div class=\"dd algo[^>]*>([\s\S]*?)<\/div><\/li>",re.I|re.M)
                h3 = re.compile(r"<h3[^>]*>([\s\S]*?)<\/h3>",re.I|re.M)
                abstr = re.compile(r"<div\sclass=\"compText aAbs\"[^>]*>([\s\S]*?)<\/div>",re.I|re.M)
                f = pas.findall(self.content)
                artice = ""
                for i in f:
                        title = h3.search(i).group(1)
                        content = abstr.search(i).group(1)
                        title = "<"+ttag+">"+re.sub(r'<[^>]+>','',title)+"</"+ttag+">\n"
                        content = "<"+ctag+">"+re.sub(r'<[^>]+>','',content)+"</"+ctag+">\n"
                        artice = artice + title + content
                if ( len(artice) < 5 or artice == "None"):
                        return False
                else:
                        return artice
                        
if __name__ == "__main__":
    sys.exit()
