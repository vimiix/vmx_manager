#coding=utf-8
from __future__ import unicode_literals
from django.db import models

#用户表
class Userinfo(models.Model):
    name = models.CharField(unique=True, max_length=128, verbose_name='用户名')
    password = models.CharField(max_length=128, verbose_name='用户密码')
    email = models.EmailField(verbose_name='邮箱')

#此表待启用
class Group(models.Model):
    name = models.CharField(max_length=128, verbose_name='组名')
    description = models.TextField(verbose_name='组描述')

#此表待启用
class Permission(models.Model):
    name = models.CharField(max_length=128, verbose_name='权限名')
    description = models.TextField(verbose_name='权限描述')

#主机表
class Hostinfo(models.Model):
    host_name = models.CharField(max_length=64, verbose_name='主机名')
    ip = models.CharField(max_length=32, verbose_name='IP')
    os = models.CharField(max_length=128, verbose_name='操作系统')
    cpu = models.CharField(max_length=128, verbose_name='CPU型号')
    last_login_time = models.CharField(max_length=128, verbose_name='最近登录时间')
    delete_flag = models.BooleanField(verbose_name='删除标志')







