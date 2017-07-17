#coding=utf-8
import hashlib

from django.shortcuts import render, HttpResponseRedirect
from remoteCMD.remote import Remote
from .models import *


def _hash_password(password):
    '''
    md5加密
    :param password:
    :return: 加密后的字符串
    '''
    md5 = hashlib.md5()
    md5.update(password)
    return md5.hexdigest()

def _is_user_exist(username):
    '''
    检测用户名是否存在
    :param username:
    :return: bool
    '''
    if Userinfo.objects.filter(name = username):
        return True
    else:
        return False

def _login_check(func):
    '''
    用户登陆验证
    :param func:
    :return: 如果有登录，返回原请求，如果未登录，重定向到登录页
    '''
    def check(req, *a, **k):
        name = req.COOKIES.get("name")
        if not name:
            return HttpResponseRedirect('/manager/login')
        return func(req, *a, **k)
    return check

def login(req):
    if req.method == 'POST' and req.POST:
        username = req.POST['username']
        password = req.POST['password']
        password = _hash_password(password)

        if (_is_user_exist(username)):
            dbpassword = Userinfo.objects.get(name=username).password
            if dbpassword == password:
                response = HttpResponseRedirect('/manager/index')
                response.set_cookie('name', username, max_age=3600)
                req.session['name'] = username
                return response
            else:
                error = '用户名或密码错误，请重新输入'
                return render(req, 'login.html', locals())
        else:
            error = '用户名或密码错误，请重新输入'
            return render(req, 'login.html', locals())
    else:
        return render(req, 'login.html', locals())

def logout(req):
    req.session.clear()
    response = HttpResponseRedirect('/manager/login')
    response.delete_cookie('name')
    return response

def register(req):
    if req.method == 'POST' and req.POST:
        username = req.POST['username']
        if _is_user_exist(username):
            warning = '用户名已存在，请重新选一个独特的用户名'
            return render(req, 'register.html', locals())
        user = Userinfo()
        user.name = username
        user.password = _hash_password(req.POST['password'])
        user.email = req.POST['email']
        user.save()
        return HttpResponseRedirect('/manager/login')
    else:
        return render(req, 'register.html')

@_login_check
def index(req):#首页
    username = req.COOKIES.get('name','')
    return render(req,'index.html', locals())

@_login_check
def hostlist(req):#主机列表信息
    username = req.COOKIES.get('name', '')
    host_list = Hostinfo.objects.filter(delete_flag=False)
    return render(req, 'hostlist.html', locals())

def _get_host_info(ip, admin, password, nickname):
    try:
        r = Remote(host=ip, username=admin, password=password)
        db_host = Hostinfo()
        db_host.ip = ip
        db_host.host_name = nickname
        db_host.cpu = str(r.ssh("cat /proc/cpuinfo | grep name |cut -f2 -d:")[0]).replace('\n','')
        db_host.os = str(r.ssh("cat /etc/redhat-release")[0]).replace('\n','')
        db_host.last_login_time = str(r.ssh("who -b | cut -d ' ' -f 13,14")[0]).replace('\n','')
        db_host.delete_flag = False
        db_host.save()
        return True
    except Exception as e:
        print e
        return False

@_login_check
def add_host(req):#新增主机
    username = req.COOKIES.get('name', '')
    if req.method == 'POST' and req.POST:
        host_ip = req.POST['ip']
        admin = req.POST['admin']
        password = req.POST['password']
        nickname = req.POST['nickname']
        if _get_host_info(host_ip, admin, password, nickname):
            is_add_success = 1
            return render(req, 'add_host.html', locals())
        else:
            is_add_success = 2
            return render(req, 'add_host.html', locals())
    return render(req, 'add_host.html')

@_login_check
def del_host(req):
    search_id = req.GET.get('id','')
    host = Hostinfo.objects.get(id=search_id)
    host.delete_flag = True
    host.save()
    return HttpResponseRedirect('/manager/hostlist')


@_login_check
def disk_ctl(req):
    username = req.COOKIES.get('name', '')
    return render(req, 'disk_ctl.html', locals())


