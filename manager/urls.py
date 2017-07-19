#coding=utf-8
from django.conf.urls import url
from .views import *
from showdata.views import *
from remoteCMD.views import *

urlpatterns = [
    url(r'^$', index),
    url(r'^(?i)index/', index, name='index'),
    url(r'^(?i)login/', login, name='login'),
    url(r'^(?i)register/', register, name='register'),
    url(r'^(?i)logout/', logout, name='logout'),
    url(r'^(?i)hostlist/', hostlist, name='hostList'),
    url(r'^(?i)del_host/', del_host, name='del_host'),
    url(r'^(?i)add_host/', add_host, name='add_host'),
    url(r'^(?i)remote_cmd/', remote_cmd, name='remote_cmd'),
    url(r'^(?i)show_data/', showData, name='showData'),
    url(r'^(?i)saveData/', saveData, name='saveData'),
    url(r'^(?i)getData/', getData, name='getData'),
    url(r'^(?i)file_trans/', file_trans, name='filetrans')
]