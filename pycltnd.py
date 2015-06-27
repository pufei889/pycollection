#!/usr/bin/env python
# -*- coding: utf-8 -*-
#author Hito http://www.hitoy.org/
import os,sys,time,urllib,post,yahoo,ask,bing,wow

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
    sys.stdout.write("Must Input a Target URL -u url\n")
    sys.exit()

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
        count = int(arguments[c])
    except:
        count = 20

if ("getyahoo" in arguments):
    engine = 'yahoo'
elif ("getbing" in arguments):
    engine = 'bing'
elif ("getwow" in arguments):
    engine = 'wow'
else:
    engine = 'ask'

try:
    keyhd=open(keyfile,'r')
except:
    sys.stdout.write("Can not open %s\n"%keyfile)
    sys.exit()

#run as deamon 
if ( "-d" in arguments ):
    try:
        pid = os.fork()
    except:
        sys.stdout.write("Your System are not support to run as deamon\n")
        sys.exit()
    
    if pid:sys.exit()
    logfd = open(logfile,'a+')
    os.dup2(logfd.fileno(),0)
    os.dup2(logfd.fileno(),1)
    os.dup2(logfd.fileno(),2)
    os.close(logfd.fileno())
    os.setsid()
    os.umask(0)
    os.chdir("/")
        
"""main"""
while True:
    key = keyhd.readline()
    if not key:break
    key=key.strip()
    if len(key) == 0: continue
    post_content = ''
    
    try:
        ## GET CONTENT
        if engine == 'yahoo':
            rurl="https://search.yahoo.com/search?p=%s&n=%s"%(urllib.quote(key),count)
            YaCo=yahoo.Yahoo(rurl,'https://www.yahoo.com/')
            post_content = YaCo.filter()

        elif engine == 'wow':
            for i in range(count/10):
                page = str(i)
                rurl="http://www.wow.com/search?q=%s&page=%s"%(urllib.quote(key),page)
                WoCo=wow.Wow(rurl,'http://www.wow.com/')
                post_content = post_content + WoCo.filter()

        elif engine == 'ask':
            for i in range(count/10):
                page = str(i)
                rurl="http://www.ask.com/web?q=%s&page=%s"%(urllib.quote(key),page)
                AsCo=ask.Ask(rurl,'http://www.ask.com/')
                post_content = post_content + AsCo.filter()
            
        elif engine == 'bing':
            for i in range(count/10):
                page = str(i+1)
                rurl="http://www.bing.com/search?q=%s&first=%s"%(urllib.quote(key),page)
                YaCo=bing.Bing(rurl,'http://www.bing.com/')
                post_content = post_content + YaCo.filter()
        
        ##POST CONTENT
        if (post_content and len(post_content) > 10 ):
                    try:
                        pl="%s?action=save&secret=yht123hito"%posturl
                        result=post.POST(pl,{"post_title":key,"post_content":post_content}).strip()
                        sys.stdout.write(("[%s] - %s - %s\n")%(time.ctime(),key,result))
                    except:
                        sys.stdout.write(("[%s] - %s - %s\n")%(time.ctime(),key,'publish Failure'))
        else:
            sys.stdout.write(("[%s] - %s - %s\n")%(time.ctime(),key,"Collection Failure"))
        sys.stdout.flush()
        time.sleep(interval)
    except KeyboardInterrupt:
        sys.stdout.write(("[%s] - %s\n")%(time.ctime(),"Exit: User Termination"))
        break
    except:
        pass
#close
sys.exit(0)
