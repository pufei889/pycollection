#!/usr/bin/env python
from collection import Collection
import re
import HTMLParser
h = HTMLParser.HTMLParser()

class Ask(Collection):
    def filter(self,ttag="h2",ctag="p"):
                
                if not self.content : return
                pas = re.compile(r"<div[\s]class=\"wresult[\s]tsrc_tled\">([\s\S]*?)<\/div>",re.I|re.M)
                h3 = re.compile(r"<h3[^>]+>([\s\S]*?)<\/h3>",re.I|re.M)
                abstr = re.compile(r"<p[\s]class=\"abstract[\s]txt3\"[^>]+>([\s\S]*?)<\/p>",re.I|re.M)
                f = pas.findall(self.content)
                artice = ""
                for i in f:
                        title = h3.search(i).group(1)
                        content = abstr.search(i).group(1)
                        title = "<"+ttag+">"+h.unescape(re.sub('<[^>]+>','',title))+"</"+ttag+">\n"
                        content = "<"+ctag+">"+h.unescape(re.sub('<[^>]+>','',content))+"</"+ctag+">\n"
                        artice = artice + title + content
                if ( len(artice) < 5 or artice == "None"):
                        return False
                else:
                        return artice.replace('\n','').encode('utf-8')
                        
if __name__ == "__main__":
      print "This is not a Direct execut program "
