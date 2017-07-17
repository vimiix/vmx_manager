#coding=utf-8
from django.db import models

class CmdList(models.Model):
    cmd = models.CharField(max_length=128, verbose_name='命令')
    host = models.CharField(max_length=64, default='192.168.59.129',verbose_name='主机')
    time = models.DateTimeField(verbose_name='发出命令时间')