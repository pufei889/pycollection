#!/usr/bin/env python
# -*- coding: utf-8 -*-
#author Hito http://www.hitoy.org/
import os,sys,time,post,yahoo,ask,urllib

"""
arguments:
-u:    POST url, needed
-k:   key file name should be a path   defalut  key.txt
-t:   collection and pulish interval seconds       defalut  5 seconds
-c:   Special for get yahoo content, list content  10 ,20 or 30 default 20
-d:    For linux with -d , you can run this progarm as deamon
"""

logfile   = "./pycltnd.log"
keyfile = "./key.txt"

arguments = sys.argv
count=20
interval = 10
if ( "-u" in arguments ):
    u = arguments.index("-u")+1
    posturl = arguments[u]
else:
    print "Must Input a Target URL -t url"
    sys.exit(0)

if ( "-k" in arguments ):
    k = arguments.index("-k")+1
    keyfile = arguments[k]

if ( "-t" in arguments ):
    t = arguments.index("-t")+1
    try:
        interval = int(arguments[t])
    except:
        interval = 10

if ( "-c" in arguments ):
    c = arguments.index("-c")+1
    try:
        count = arguments[c]
    except:
        count=20

if ("getyahoo" in arguments):
    getyahoo = True
else:
    getyahoo = False

try:
    keyhd=open(keyfile,'r')
except:
    print "Can not open %s"%keyfile

#run as deamon 
if ( "-d" in arguments ):
    try:
        pid = os.fork()
    except:
        print "Your System are not support to run as deamon"
    
    if pid:sys.exit()
    os.setsid()
    os.umask(0)
    os.chdir("/")
    try:
        logfd = open(logfile,'a')
        os.dup2(logfd.fileno(),0)
        os.dup2(logfd.fileno(),1)
        os.dup2(logfd.fileno(),2)
        os.close(logfd.fileno())
    except:
        print "Can not Access %s"%logfile

        
"""main"""
while True:
    try:
        key = keyhd.readline().strip()
        if len(key) == 0: break
        post_content = ''
        if not getyahoo:
            for i in range(count/10):
                page = str(i+1)
                asurl="http://www.ask.com/web?q=%s&page=%s"%(urllib.quote(key),page)
                AsCo=ask.Ask(asurl,'http://www.ask.com/')
                post_content = post_content + AsCo.filter().encode('utf-8')
        else:
            geturl="https://search.yahoo.com/search?p=%s&n=%s"%(urllib.quote(key),count)
            YaCo=yahoo.Yahoo(geturl)
            post_content = YaCo.filter().encode('utf-8')
        if (len(post_content) > 10 ):
                    try:
                        pl="%s?action=save&secret=yht123hito"%posturl
                        result=post.POST(pl,{"post_title":key,"post_content":post_content})
                        sys.stdout.write(("[%s] - %s - %s\n")%(time.ctime(),key,result))
                    except:
                        sys.stdout.write(("[%s] - %s - %s\n")%(time.ctime(),key,'publish Failure'))
        else:
            sys.stdout.write(("[%s] - %s - %s\n")%(time.ctime(),key,"Collection Failure"))
            
        sys.stdout.flush()
        time.sleep(interval)
    except KeyboardInterrupt,e:
        break
    
#close
print "Task Complete"
keyhd.close()
