#!/usr/bin/env python
# -*- coding: utf-8 -*-

import urllib2,StringIO,sys
from urllib import quote
from  xml.dom import  minidom
reload(sys)
sys.setdefaultencoding('utf-8')
class Yandex():
    def __init__(self,query,page=1,lang="en",uname="hitoy2015",key="03.342224283:96c3252026935a65f6cc0475cedf3519"):
        searchurl="https://yandex.com/search/xml?user=%s&key=%s&query=%s&l10n=%s&page=%s"%(uname,key,quote(query),lang,page)
        self.content = urllib2.urlopen(searchurl).read().replace("<hlword>","").replace("</hlword>","")
    
    def filter(self,ttag="h2",ctag="p"):
        artice = ''
        dom = minidom.parse(StringIO.StringIO(self.content)).documentElement
        nodelist = dom.getElementsByTagName('group')
        for node in nodelist:
            try:
                h2 = "<%s>%s</%s>" %(ttag, node.getElementsByTagName('title')[0].firstChild.data,ttag)
                p = "<%s>%s</%s>" % (ctag, node.getElementsByTagName('passage')[0].firstChild.data,ctag)
                artice = artice + "%s\r\n%s\r\n" % (h2,p)
            except:
                pass
        return artice
    
if __name__ == "__main__":
    sys.exit()
    
