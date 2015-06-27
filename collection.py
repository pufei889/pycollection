#!/usr/bin/env python
import urllib2,urllib,sys

class Collection:
    __referer = "http://www.google.com/"
    __useragent = "Mozilla/5.0 (Windows NT 6.3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/33.0.1750.149 Safari/537.36"
    
    def __init__(self,url,referer=__referer,ua=__useragent):
        self.__ua = ua
        self.__referer = referer
        try:
            self.content = self.__get_content(url)
        except:
            self.content = ""

    def __get_content(self,url):
        header = {"Accept": "text/plain","Connection":"close","User-Agent":self.__ua,"Referer":self.__referer}
        req = urllib2.Request(url,headers=header)
        page = urllib2.urlopen(req,timeout=10)
        return page.read().strip()
        


if __name__ == "__main__":
    sys.exit()
