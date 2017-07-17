#coding=utf-8
from django.shortcuts import render
from django.http import JsonResponse
from manager.views import _login_check

# Create your views here.

from .models import CPUData

#接收客户端主机POST方式发送过来的数据
def saveData(req):
    result = {'status':'error', 'err_msg':''}
    if req.method == 'POST' and req.POST:
        data = req.POST['data']
        time = req.POST['time']

        cpu = CPUData()
        cpu.data = data
        cpu.time = time
        cpu.save()
        result['status'] = 'success'
        result['err_msg'] = 0
    else:
        result['err_msg'] = 'request method must be POST, not null'
    return JsonResponse(result)

#读取数据库中最新的一条数据
def getData(req):
    data = CPUData.objects.order_by('-id')[0]
    time = data.time
    result = {
        'time':time.strftime('%H:%M:%S'),
        'data':data.data
    }
    return JsonResponse(result)

@_login_check
def showData(req):
    return render(req, 'show_data.html')