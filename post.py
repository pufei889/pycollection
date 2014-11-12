#!/usr/bin/env python
import urllib2,urllib

def POST(url,data):
    formdata=urllib.urlencode(data)
    req = urllib2.Request(url,headers={'User-Agent' : "Magic Browser"}) 
    f = urllib2.urlopen(req,formdata,timeout=10)
    content = f.read()
    return content


if __name__ == "__main__":
    print "Can not be excute"
