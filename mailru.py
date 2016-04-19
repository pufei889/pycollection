#!/usr/bin/env python
# -*- coding=utf-8 -*-
from collection import Collection
import re,sys
class Mailru(Collection):
    def filter(self,ttag="h2",ctag="p"):
        pas = re.compile(r"{\"srch_id\":([\s\S]*?)\"is_navig\":",re.I|re.M)
        h3 = re.compile(r"\"title\":\"([\s\S]*?)\",",re.I|re.M)
        abstr = re.compile(r"\"passage\":\"([\s\S]*?)\",",re.I|re.M)
        f = pas.findall(self.content)
        if not f: return ""
        artice = ""
        for i in f:
            try:
                title = h3.search(i).group(1).decode('unicode_escape') if h3.search(i) else ''
                content = abstr.search(i).group(1).decode('unicode_escape') if abstr.search(i) else ''
                content = re.sub(r"<span[^>]*>.*?<\/span>","",content)
                title = "<"+ttag+">"+re.sub(r'<[^>]+>','',title)+"</"+ttag+">\n"
                content = "<"+ctag+">"+re.sub(r'<[^>]+>','',content)+"</"+ctag+">\n"
                artice = artice + title + content
            except:
                pass
        if ( len(artice) < 5 or artice == "None"):
            return ""
        else:
            return artice.encode("utf-8")
                        
if __name__ == "__main__":
    sys.exit()
