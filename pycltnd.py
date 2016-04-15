#!/usr/bin/env python
# -*- coding: utf-8 -*-
#author Hito http://www.hitoy.org/
import os,sys,time,urllib,signal,post,yahoo,ask,bing,wow,ecosia,yandex,coccoc,izito,lycos,baidu,haosou,search

sysnote="""
Author	Hito
Blog	https://www.hitoy.org/
Update	2016.04.06
"""
sys.stdout.write(sysnote)
"""
arguments:
-u:    POST url, needed
-k:   key file name should be a path   defalut  key.txt
-t:   collection and pulish interval seconds       defalut  5 seconds
-c:   Special for get yahoo content, list content  10 ,20 or 30 default 20
-d:    For linux with -d , you can run this progarm as deamon
"""

logfile   = "./pycltnd.log"
errfile   = "./pycltnd.err"
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

if ("getask" in arguments):
    engine = 'ask'
elif ("getbing" in arguments):
    engine = 'bing'
elif ("getecosia" in arguments):
    engine = 'ecosia'
elif ("getwow" in arguments):
    engine = 'wow'
elif ("getyandex" in arguments):
    engine = 'yandex'
elif ("getcoccoc" in arguments):
	engine = 'coccoc'
elif ("getizito" in arguments):
    engine = 'izito'
elif ("getlycos" in arguments):
    engine = 'lycos'
elif ("getbaidu" in arguments):
    engine = 'baidu'
elif ("gethaosou" in arguments):
    engine = 'haosou'
elif ("getsearch" in arguments):
    engine = 'search'
else:
    engine = 'yahoo'

try:
    keyhd=open(keyfile,'rb')
except:
    sys.stdout.write("Can not open %s\n"%keyfile)
    sys.exit()

#run as deamon 
if ( "-d" in arguments ):
    try:
        pid = os.fork()
        logfd = open(logfile,"a+")
        errfd = open(errfile,"a+")
        os.close(0)
        os.dup2(logfd.fileno(),1)
        os.dup2(errfd.fileno(),2)
        logfd.close()
        errfd.close()
    except:
        sys.stdout.write("Your System are not support to run as deamon\n")
        sys.exit()

    if pid:sys.exit()
    os.setsid()
    os.umask(0)
    os.chdir("/")


"""main"""
while True:
    key = keyhd.readline()
    if not key:break
    key=key.strip().lstrip("\xef\xbb\xbf")
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

        elif engine == 'ecosia':
            for i in range(count/10):
                page = str(i)
                rurl="https://www.ecosia.org/search?p=%s&q=%s"%(page,urllib.quote(key))
                EcCo=ecosia.Ecosia(rurl,'https://www.ecosia.org/')
                post_content = post_content + EcCo.filter()
                
        elif engine == 'yandex':
            for i in range(count/10):
                page = str(i)
                yanCo = yandex.Yandex(key,page)
                post_content = post_content + yanCo.filter()
        elif engine == 'coccoc':
            for i in range(count/10):
                page  = str(i)
                rurl = "http://coccoc.com/composer?q=%s&p=%s"%(urllib.quote(key),page)
                coccocO = coccoc.Coccoc(rurl,"http://coccoc.com/search")
                post_content = post_content + coccocO.filter()
        elif engine == 'izito':
            for i in range(count/10):
                page = str(i+1)
                rurl = "http://www.izito.com/?query=%s&pg=%s"%(urllib.quote(key),page)
                izitoO = izito.Izito(rurl,"http://www.izito.com/")
                post_content = post_content + izitoO.filter()
        elif engine == 'lycos':
            for i in range(count/10):
                page = str(i+1)
                rurl = "http://search.lycos.com/web/?q=%s&pn=%s"%(urllib.quote(key),page)
                lycosO= lycos.Lycos(rurl,"http://search.lycos.com/")
                post_content = post_content + lycosO.filter()
        elif engine == 'baidu':
            for i in range(count/10):
                page = str(count - 10);
                rurl = "https://www.baidu.com/s?wd=%s&pn=%s"%(urllib.quote(key),page)
                baiduO= baidu.Baidu(rurl,"https://www.baidu.com/")
                post_content = post_content + baiduO.filter()
        elif engine == 'haosou':
            for i in range(count/10):
                page = str(i+1)
                rurl = "https://www.so.com/s?q=%s&pn=%s"%(urllib.quote(key),page)
                haosouO= haosou.So(rurl,"https://www.so.com")
                post_content = post_content + haosouO.filter()
        elif engine == 'search':
            for i in range(count/10):
                page = str(i+1)
                rurl = "https://www.search.com/web?q=%s&page=%s"%(urllib.quote(key),page)
                searchCo = search.Search(rurl,"https://www.search.com/")
                post_content = post_content + searchCo.filter()
        time.sleep(interval)
    except KeyboardInterrupt:
        sys.stdout.write(("[%s] - %s\n")%(time.ctime(),"Exit: User termination"))
        break

    ##POST CONTENT
    if (post_content and len(post_content) > 10 ):
        try:
            pl="%s?action=save&secret=yht123hito"%posturl
            result=post.POST(pl,{"post_title":key,"post_content":post_content}).strip()
            sys.stdout.write(("[%s] - %s - %s\n")%(time.ctime(),key.decode("utf-8"),result.decode("utf-8")))
        except Exception,e:
			sys.stdout.write(("[%s] - %s - %s:%s\n")%(time.ctime(),key.decode("utf-8"),'publish Failure',e))
    else:
        sys.stdout.write(("[%s] - %s - %s\n")%(time.ctime(),key.decode("utf-8"),"Collection Failure"))

    sys.stdout.flush()
#close
sys.exit(0)
