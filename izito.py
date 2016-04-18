#!/usr/bin/env python
# -*- coding: utf-8 -*-
from collection import Collection
import re,sys
class Izito(Collection):
    def filter(self,ttag="h2",ctag="p"):
        pas = re.compile(r"<li\sclass=\"searchresult\"[^>]*>([\s\S]*?)<\/li>",re.I|re.M)
        h3 = re.compile(r"<h3>([\s\S]*?)<\/h3>",re.I|re.M)
        abstr = re.compile(r"<p>([\s\S]*?)<\/p>",re.I|re.M)
        f = pas.findall(self.content)
        if not f: return ""
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
    a = Izito("http://www.izito.com/?vid=l21828140190I1460943666&sess=a3a3a303a3a313&template=&asid=1810073229&awc=&de=&nwc=&suggest=1&q=steam+boilers")
    print a.content
    print a.filter()
    sys.exit()
