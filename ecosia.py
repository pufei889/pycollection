#!/usr/bin/env python
# -*- coding: utf-8 -*-
from collection import Collection
import re,sys
class Ecosia(Collection):
    def filter(self,ttag="h2",ctag="p"):
        pas = re.compile(r"<div class=\"result js-result card-mobile\">([\s\S]*?)<\/p>",re.I|re.M)
        h3 = re.compile(r"<a[^>]*>([\s\S]*?)<\/a>",re.I|re.M)
        abstr = re.compile(r"<p\sclass=\"result-snippet\">([\s\S]+)$",re.I|re.M)
        f = pas.findall(self.content)
        if not f: return ""
        artice = ""
        for i in f:
            try:
                title = h3.search(i).group(1).strip() if h3.search(i) else ''
                content = abstr.search(i).group(1).strip() if abstr.search(i) else ''
                if title == '' or content=='':
                    continue
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
	sys.exit(-1)
