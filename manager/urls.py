#coding=utf-8
from django.conf.urls import url
from .views import *
from showdata.views import *
from remoteCMD.views import *

urlpatterns = [
    url(r'^$', index),
    url(r'^index/', index, name='index'),
    url(r'^login/', login, name='login'),
    url(r'^register/', register, name='register'),
    url(r'^logout/', logout, name='logout'),
    url(r'^hostlist/', hostlist, name='hostList'),
    url(r'^del_host/', del_host, name='del_host'),
    url(r'^add_host/', add_host, name='add_host'),
    url(r'^remote_cmd/', remote_cmd, name='remote_cmd'),
    url(r'^show_data/', showData, name='showData'),
    url(r'^saveData/', saveData, name='saveData'),
    url(r'^getData/', getData, name='getData'),
    url(r'^file_trans/', file_trans, name='filetrans')
]