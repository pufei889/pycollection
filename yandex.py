#!/usr/bin/env python
# -*- coding: utf-8 -*-

import urllib2,StringIO,sys
from urllib import quote
from  xml.dom import  minidom

class Yandex():
    def __init__(self,query,page=0):
        searchurl="http://lab.hitoy.org/api/searchapi/yandex.php?q=%s&page=%s"%(quote(query),page)
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
        return artice.encode("utf-8")
    
if __name__ == "__main__":
    sys.exit()
    
