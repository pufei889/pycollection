#!/usr/bin/env python
from collection import Collection
import re,sys

class Ask(Collection):
    def filter(self,ttag="h2",ctag="p"):
                
                if not self.content : return
                pas = re.compile(r"<div\sclass=\"web-result\sur\stsrc_tled[^>]*>([\s\S]*?)<\/div>",re.I|re.M)
                h3 = re.compile(r"<h2[^>]+>([\s\S]*?)<\/h2>",re.I|re.M)
                abstr = re.compile(r"<p[\s]class=\"web-result-description\">([\s\S]*?)<\/p>",re.I|re.M)
                f = pas.findall(self.content)
                artice = ""
                for i in f:
                        title = h3.search(i).group(1).strip()
                        content = abstr.search(i).group(1).strip()
                        title = "<"+ttag+">"+re.sub('<[^>]+>','',title)+"</"+ttag+">\n"
                        content = "<"+ctag+">"+re.sub(r'[\r\n]*','',re.sub(r'^\d+[\w\s]*...','',re.sub('<[^>]+>','',content)))+"</"+ctag+">\n"
                        artice = artice + title + content
                if ( len(artice) < 5 or artice == "None"):
                        return False
                else:
                        return artice
                        
if __name__ == "__main__":
    sys.exit()
