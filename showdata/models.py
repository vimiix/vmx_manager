#coding=utf-8
from django.db import models

class CPUData( models.Model ):
    data = models.CharField(max_length=132, verbose_name='CPU数据')
    time = models.DateTimeField(verbose_name='监听时间')

