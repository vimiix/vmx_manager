#!/usr/bin/python
#coding:utf-8

#提示:将本文件分发到要监测的客户端主机上运行

import time
import datetime
import urllib
import urllib2

import psutil

url = "http://192.168.1.109:8000/manager/saveData/"


headers = {
    "User-Agent":"Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.133 Safari/537.36"
}
while True:
    data = {
        "data":psutil.cpu_times().system,
        "time":datetime.datetime.now()
    }
    sendData = urllib.urlencode(data)
    request = urllib2.Request(url,data = sendData,headers = headers)
    opener = urllib2.urlopen(request)
    reader = opener.read()
    print(reader)
    time.sleep(1)




