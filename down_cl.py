# coding=utf-8  
# -*- coding: utf-8 -*-

import re  
import urllib.request
import urllib.parse
# 导入解压模块
import gzip
import time
import os
import time
import threading

# python C:\code\python\down_cl.py

# 存储图片
# imgurl = 'http://www.wzhospital.cn/wyyy/pic/in_Png/webtit.png'
# # urllib.request.urlretrieve(imgurl, 'C:\\s.png','wb')

# f = open("2223.png", 'wb')
# f.write((urllib.request.urlopen(imgurl)).read())
# f.close()

#os.makedirs('[12.02] 店長推薦作品(SMD-159) S Model 159 Ero Body OL裏事情  こころ')

ISOTIMEFORMAT='%Y-%m-%d %X'
_g_cookieStr =  'lastupdate=1480860704; __cfduid=d9d23e778a8d5aa99977bc1deb136080d1480692603; aafaf_ol_offset=97; aafaf_lastpos=F5; aafaf_lastvisit=137%091480860707%09%2Fpw%2Fthread.php%3Ffid%3D5%26page%3D4%26ty%3D6667; aafaf_threadlog=%2C3%2C5%2C; a0888_pages=2; a0888_times=5'
#获取网页




time_count=2 # 连续10次下载不过来就不下载了
dothreads_count=0
def getAAll(content):
    res = r'<h3><a.*?href=.*?<\/a></h3>'  
    mm =  re.findall( res, content, re.S|re.M)  
    val=''
    for value in mm:  
        val=value
    return val

def getAContent(content):
    res = r'<a .*?>(.*?)</a>'  
    mm =  re.findall( res, content, re.S|re.M)  
    val=''
    for value in mm:  
        val=value
    return val

def getAHref(content):
    res = r'(?<=href=\").+?(?=\")|(?<=href=\').+?(?=\')'  
    mm =  re.findall( res, content, re.S|re.M)  
    val=''
    for value in mm:  
        val=value
    return val

def setCookies(headers):
    # 找到Set-Cookie
    global _g_cookieStr 
    _is_load=False
    _g_cookies=_g_cookieStr.split('; ')
    for _sc in headers:
        if _sc=='Set-Cookie':
            v_set_cookie=headers[_sc] # 就是：aafaf_threadlog=%2C3%2C5%2C; expires=Mon, 04-Dec-2017 13:03:54 GMT; path=/; httponly
            v_set_cookies=v_set_cookie.split('; ') #aafaf_threadlog=%2C3%2C5%2C
            for v_set_cookies_c in v_set_cookies:
                _temp_v_set_cookies_c=v_set_cookies_c.split('=')
                if len(_temp_v_set_cookies_c)>1: # _temp_v_set_cookies_c=['aafaf_threadlog','%2C3%2C5%2C']
                    _g_cookies_temp=[]
                    for _cooks in _g_cookies:
                        if _cooks.startswith(_temp_v_set_cookies_c[0])==True:
                            _is_load=True
                            _g_cookies_temp.append('='.join(_temp_v_set_cookies_c))
                        else:
                            _g_cookies_temp.append(_cooks)
                    _g_cookies=_g_cookies_temp
    if _is_load==True:
        _g_cookieStr='; '.join(_g_cookies)

def getHtml(url,ii):
    if ii>time_count:
        return ''
    ii=ii+1
    try:
        req = urllib.request.Request(url)
        req.add_header('Accept', 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8')
        req.add_header('Accept-Encoding', 'gzip, deflate, sdch')
        req.add_header('Accept-Language', 'zh-CN,zh;q=0.8,en-US;q=0.6,en;q=0.4')
        req.add_header('Cache-Control', 'max-age=0')
        print('最新cookies:{0}'.format(_g_cookieStr))
        req.add_header('Cookie', _g_cookieStr)
        req.add_header('Host', '1024.91lulea.biz')
        req.add_header('Proxy-Connection', 'keep-alive')
        req.add_header('Upgrade-Insecure-Requests', '1')
        req.add_header('User-Agent', 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.99 Safari/537.36')
        print('正在下载html信息------------------------------------')
        response = urllib.request.urlopen(req) 
        setCookies(response.headers)
        print('下载完成html信息------------------------------------')
        decompressHtml=gzip.decompress(response.read())
        decompressHtml=decompressHtml.decode('utf-8', 'ignore') #加上 ignore 忽略错误编码
        print('html下载完成:{0}'.format(url))
        printDateTime()
        return decompressHtml
    except Exception as err:
        print('有异常：')
        print(err)
        print('-----------------------------------')
        time.sleep(0.2)
        return getHtml(url,ii)
    
# 返回主题
def getChildrenCore(html):
    res_tr = r'<div class="tpc_content" id="read_tpc">(.*?)</div>'
    m_tr =  re.findall(res_tr,html,re.S|re.M)
    val=''
    for line in m_tr: 
        val=line
    return val

def doChildrenHtmlfilter_tags(html):
    html=html.replace('<br>','\r\n')
    html=html.replace('&nbsp;','')
    return html

def saveIamge(line, imagePath,ii):
    if ii>time_count:
        return ''
    ii=ii+1
    try:
        # line='http://www.wzhospital.cn/wyyy/web/yydt/showBlobPic2.aspx?id=194171'
        # urllib.request.urlretrieve(line, "dd.jpg",'wb')
        # socket.setdefaulttimeout(2) # 2秒超时
        req = urllib.request.Request(line)
        req.add_header('User-Agent','Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.99 Safari/537.36')
        # req.add_header('Accept','text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8')
        # req.add_header('Accept-Language','adzh-CN,zh;q=0.8,en-US;q=0.6,en;q=0.4fadf')
        # req.add_header('Cookie','__cfduid=dd957d8588bca854d5d281f4c825df75d1480702520')
        # req.add_header('Accept','adfadf')
        # req.add_header('Accept','adfadf')
        print('正在下载Image信息------------------------------------')
        page = urllib.request.urlopen(req,timeout=10).read() # 设置超时时间
        file = open(imagePath, 'wb')
        file.write(page)
        print('已保存Image信息成功 ------------------------------------')
        file.close()
        print('图片下载完成 {0}'.format(line))
        printDateTime()
    except Exception as err:
        print('图片保存异常：')
        print(err)
        print(line)
        print('-----------------------------------')
        time.sleep(0.2)
        saveIamge(line, imagePath,ii)


def saveImg(html,path):
    res_tr = r'<img src="(.*?)"'
    m_tr =  re.findall(res_tr,html,re.S|re.M)
    for line in m_tr: # 获取到image地址
        arr=line.split('/')
        imgName=arr[len(arr)-1]
        imagePath='{0}\\{1}'.format(path,imgName)
        if os.path.isfile(imagePath)==False:
            saveIamge(line, imagePath,0)
        
    

def doChildrenHtml(html,path,urlPath,childrenUrl):
    body=getChildrenCore(html)
    content=doChildrenHtmlfilter_tags(body)
    saveImg(content,path)
    fh = open(urlPath, 'w')
    fh.write('{0}\r\n地址：{1}'.format(content,childrenUrl) )
    fh.close() 
    print('子页面下载完成：{0}'.format(childrenUrl))
    
def dothreads(line):
    all=getAAll(line)
    title=getAContent(all).replace(':','')
    href=getAHref(all)
    global dothreads_count 
    dothreads_count=dothreads_count+1
    if title.startswith('<font')==False:
        print('开始执行第{0}个线程 ---------'.format(dothreads_count))
        path='1024\{0}'.format(title)
        urlPath='1024\\{0}\\url.txt'.format(title)
        if os.path.exists(path)==True and os.path.isfile(urlPath)==True: # os.path.exists(path)==True and os.listdir(path)==True:
            print('已存在该文件夹及文件：{0} =================='.format(path))
            return
        elif os.path.exists(path) == False:
            os.makedirs(path)
            print('创建文件:{0}'.format(path))
        childrenUrl='{0}{1}'.format(rootUrl,href)# 子页面url
        doChildrenHtml(getHtml(childrenUrl,0),path,urlPath,childrenUrl) # 处理子页面url
        print('子页面处理完成：{0}'.format(path))
        print('第{0}个线程【执行完毕】 ---------'.format(dothreads_count))
        printDateTime()

def groupthread(m_tr):
    for line in m_tr:
        all=getAAll(line)
        title=getAContent(all).replace(':','')
        if title.startswith('<font')==False:
            path='1024\{0}'.format(title)
            urlPath='1024\\{0}\\url.txt'.format(title)
            if os.path.exists(path)==True and os.path.isfile(urlPath)==True:
                return
            else:
                t1 = threading.Thread(target=dothreads,args=(line,))
                # threads.append(t1)
                t1.setDaemon(True)
                t1.start()
                print('开启线程：----')
    t1.join()
def printDateTime():
    print('---------------------- 当前时间：{0} --------------------------'.format(time.strftime( ISOTIMEFORMAT, time.localtime())))

printDateTime()
rootUrl='http://1024.91lulea.biz/pw/'

def doWork(url_):
    printDateTime()
    decompressHtml=getHtml(url_,0)
    res_tr = r'<tr align="center" class="tr3 t_one">(.*?)</tr>'
    m_tr =  re.findall(res_tr,decompressHtml,re.S|re.M)
    # if os.path.exists('1024'):
    #     __import__('shutil').rmtree('1024')
    threads = []
    tcount=0
    group=3 # 每五个一组
    print('一共{0}项----------'.format(len(m_tr)))

    for line in m_tr:
        tcount=tcount+1
        threads.append(line)
        if tcount%group==0:
            print('开始执行3个线程')
            groupthread(threads)
            threads = []
    groupthread(threads)
    print('开始执行最后几个线程')


pageurl='http://1024.91lulea.biz/pw/thread.php?fid=5&page={0}&ty=6366477'
for a in range(6,98,1):#range(1,5,2) #代表从1到5，间隔2(不包含5)
    doWork(pageurl.format(a))

print('----------------------【执行完成】 当前时间：{0} --------------------------'.format(time.strftime( ISOTIMEFORMAT, time.localtime())))



# python C:\code\python\down_cl.py

# fh = open('tongling12.html', 'w')  #保存string文件
# #fh = open('tongling.html', 'wb') #wb意思是保存流文件
# fh.write(stri) 
# fh.close() 

# #os.mkdir('dddfd') 