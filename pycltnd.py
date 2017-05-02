#!/usr/bin/env python
# -*- coding: utf-8 -*-
#author Hito http://www.hitoy.org/
import os,sys,time,urllib,signal,post,yahoo,ask,bing,wow,ecosia,yandex,coccoc,izito,lycos,baidu,haosou,search,duckgo,mailru,sogou,entireweb,gmx,re

sysnote="""
========================================================
==           Simulation acquisition system            ==
==    Copyright: 2017 Hito(https://www.hitoy.org/)    ==
==         Version: 0.9.3    Update: 2017.04.21       ==
========================================================
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
replacefile = False
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

if ("-r" in arguments ):
    try:
        replacefile = open(arguments[arguments.index("-r")+1],"rb")
    except Exception,e:
        sys.stdout.write("%s\n"%e)
        sys.exit()

elif (os.path.exists(os.getcwd()+'/replace.txt')):
    try:
        replacefile = open(os.getcwd()+'/replace.txt',"rb")
    except Exception,e:
        sys.stdout.write("%s\n"%e)
        sys.exit()


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
elif ("getduckgo" in arguments):
    engine = 'duckgo'
elif ("getmailru" in arguments):
    engine = 'mailru'
elif ("getsogou" in arguments):
    engine = 'sogou'
elif ("getentireweb" in arguments):
    engine =  'entireweb'
elif ("getgmx" in arguments):
    engine = 'gmx'
else:
    engine = 'yahoo'


replacere = re.compile(r"^([^\|]*)\|(.*?)$",re.I|re.S)
def key_replace(content,filefd):
    line = filefd.readline().strip().lstrip("\xef\xbb\xbf")
    while(line):
        if not line:continue
        find = replacere.search(line).group(1).strip()
        replace = replacere.search(line).group(2).strip()
        if find:
            content = content.replace(find,replace)
        line = filefd.readline()
    return content

sys.stdout.write("Use engine: %s\n\n"%engine)

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
            b=0
            for i in range(count/10):
                rurl="https://search.yahoo.com/search?p=%s&b=%d"%(urllib.quote(key),b)
                YaCo=yahoo.Yahoo(rurl,'https://www.yahoo.com/')
                post_content = post_content + YaCo.filter()
                b = post_content.count("<h2>")

        elif engine == 'bing':
            for i in range(count/10):
                page = i*10+1
                rurl="http://www.bing.com/search?q=%s&first=%d"%(urllib.quote(key),page)
                YaCo=bing.Bing(rurl,'http://www.bing.com/')
                post_content = post_content + YaCo.filter()    

        elif engine == 'yandex':
            for i in range(count/10):
                page = str(i)
                rurl="http://lab.hitoy.org/api/searchapi/yandex.php?q=%s&page=%s"%(urllib.quote(key),page)
                yanCo = yandex.Yandex(rurl,"https://www.hitoy.org/")
                post_content = post_content + yanCo.filter()

        elif engine == 'wow':
            for i in range(count/10):
                page = i+1
                rurl="http://search.wow.com/search?q=%s&page=%d"%(urllib.quote(key),page)
                WoCo=wow.Wow(rurl,'http://www.wow.com/')
                post_content = post_content + WoCo.filter()

        elif engine == 'ask':
            for i in range(count/10):
                page = i+1
                rurl="http://www.ask.com/web?q=%s&page=%d&qo=moreResults"%(urllib.quote(key),page)
                AsCo=ask.Ask(rurl,'http://www.ask.com/')
                post_content = post_content + AsCo.filter()

        elif engine == 'ecosia':
            for i in range(count/10):
                page = str(i)
                rurl="https://www.ecosia.org/search?p=%s&q=%s"%(page,urllib.quote(key))
                EcCo=ecosia.Ecosia(rurl,'https://www.ecosia.org/')
                post_content = post_content + EcCo.filter()

        elif engine == 'coccoc':
            for i in range(count/10):
                rurl = "http://coccoc.com/composer?q=%s&p=%d"%(urllib.quote(key),i)
                coccocO = coccoc.Coccoc(rurl,"http://coccoc.com/search")
                post_content = post_content + coccocO.filter()

        elif engine == 'search':
            for i in range(count/10):
                page = str(i+1)
                rurl = "https://www.search.com/web?q=%s&page=%s"%(urllib.quote(key),page)
                searchCo = search.Search(rurl,"https://www.search.com/")
                post_content = post_content + searchCo.filter()

        elif engine == 'duckgo':
            rurl = "https://duckduckgo.com/d.js?q=%s"%(urllib.quote(key))
            duckCo = duckgo.Duckgo(rurl,"https://duckduckgo.com/")
            post_content = post_content + duckCo.filter()

        elif engine == 'mailru':
            for i in range(count/10):
                page = str(i*10)
                rurl = "http://go.mail.ru/api/v1/web_search?q=%s&sf=%s"%(urllib.quote(key),page)
                mailruCo = mailru.Mailru(rurl)
                post_content = post_content + mailruCo.filter()
        
        elif engine == 'entireweb':
            for i in range(count/10):
                page = str(i*20+1)
                rurl = "http://entireweb.com/web/?q=%s&of=%s&md=web&ts=%s&gs=jH67TuiGrF68u#"%(urllib.quote(key),page,str(time.time()*1000))
                entirewebCo = entireweb.Entrieweb(rurl,"http://entireweb.com")
                post_content = post_content +  entirewebCo.filter()

        elif engine  == 'gmx':
            for i in range(count/10):
                page = str(i+1)
                rurl = "https://search.gmx.com/web?origin=serp_sf_atf&q=%s&pageIndex=%s"%(urllib.quote(key),page)
                gmxCo = gmx.Gmx(rurl,"https://www.gmx.com/")
                post_content = post_content + gmxCo.filter()

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

        elif engine == 'sogou':
            for i in range(count/10):
                page = str(i+1)
                rurl = "https://www.sogou.com/web?query=%s&page=%s"%(urllib.quote(key),page)
                sogouCo = sogou.Sogou(rurl,"https://www.sogou.com")
                post_content = post_content + sogouCo.filter()

        time.sleep(interval)
    except KeyboardInterrupt:
        sys.stdout.write(("[%s] - %s\n")%(time.ctime(),"Exit: User termination"))
        break

    ##POST CONTENT
    if (post_content and len(post_content) > 20 ):
        if replacefile:
            post_content = key_replace(post_content,replacefile)
        try:
            pl="%s?action=save&secret=yht123hito"%posturl
            result=post.POST(pl,{"post_title":key,"post_content":post_content}).strip().lstrip("\xef\xbb\xbf")
            sys.stdout.write(("[%s] - %s - %s\n")%(time.ctime(),key.decode("utf-8"),result.decode("utf-8")))
        except KeyboardInterrupt:
            sys.stdout.write(("[%s] - %s\n")%(time.ctime(),"Exit: User termination"))
            break
        except UnicodeEncodeError,e:
            sys.stdout.write(("[%s] - %s - %s\n")%(time.ctime(),key,result))
        except Exception,e:
            try:
			    sys.stdout.write(("[%s] - %s - %s:%s\n")%(time.ctime(),key.decode("utf-8"),"publish Failure",e))
            except UnicodeEncodeError:
			    sys.stdout.write(("[%s] - %s - %s:%s\n")%(time.ctime(),key,"publish Failure",e))
    else:
        try:
            sys.stdout.write(("[%s] - %s - %s\n")%(time.ctime(),key.decode("utf-8"),"Collection Failure"))
        except UnicodeEncodeError,e:
            sys.stdout.write(("[%s] - %s - %s\n")%(time.ctime(),key,"Collection Failure"))

    sys.stdout.flush()
#close
sys.exit(0)
