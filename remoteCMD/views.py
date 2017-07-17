#coding=utf-8
from django.shortcuts import render, HttpResponseRedirect
from manager.views import _login_check
from .models import CmdList
from remote import Remote, Sftp
import datetime
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
import os
from django.conf import settings

showTag = ''

#发送远程命令给客户端主机
@_login_check
def remote_cmd(req):
    username = req.COOKIES.get('name', '')
    if req.method == 'POST' and req.POST:
        #type =  req.POST.get("submit_type",None)
        if 'sendcmd' in req.POST:
            ip = req.POST['ip']
            usr = req.POST['username']
            passwd = req.POST['password']
            cmd = req.POST['cmd']
            if req.POST['port']:
                port = int(req.POST['port'])
            else:
                port = 22
            #存储到历史指令
            db_cmd = CmdList()
            db_cmd.cmd = cmd
            db_cmd.host = ip
            db_cmd.time = datetime.datetime.now()
            print db_cmd.time
            db_cmd.save()
            #远程发送指令
            handler = Remote(ip,usr,passwd,port)
            recv = handler.ssh(cmd)
            showTag = 'recv'
            return render(req, 'remote_cmd.html', locals())
        elif 'history' in req.POST:
            #查询最近8条命令
            CMDs = CmdList.objects.order_by('-id')[:8]
            result = []
            for item in CMDs:
                result.append({
                    'time': item.time.strftime('%m-%d %H:%M:%S'),
                    'cmd': item.cmd,
                    'host': item.host
                })
            showTag = 'result'
            # print result
            return render(req, 'remote_cmd.html', locals())
        else:
            return render(req, 'remote_cmd.html')
    else:
        return render(req, 'remote_cmd.html')


#和客户端主机之间的文件传输
@_login_check
def file_trans(req):
    username = req.COOKIES.get('name', '')
    if req.method == 'POST' and req.POST:
        if 'upload' in req.POST:#文件上传
            if 'upload_file' in req.FILES:
                fileObj = req.FILES.get('upload_file','')
                savePath = default_storage.save('../vmx_manager/upload/'+fileObj.name, ContentFile(fileObj.read()))
                tmpfile = os.path.join(settings.BASE_DIR,savePath)
                is_success = True
                tip_info = '上传成功'
                return render(req, 'file_trans.html', locals())
            else:
                is_success = False
                tip_info = '上传失败'
                return render(req, 'file_trans.html', locals())
        elif 'put' in req.POST:#文件分发
            hostip = req.POST['des_ip']
            clientuser = req.POST['client_user']
            clientpasswd = req.POST['client_passwd']
            put_file_path = req.POST['put_file_path']
            save_path = req.POST['save_path']

            sftp = Sftp(hostip, clientuser,clientpasswd)
            try:
                if save_path:
                    sftp.put(put_file_path, save_path)
                else:
                    sftp.put(put_file_path)
                put_success = True
                put_info = '发送成功'
                return render(req, 'file_trans.html', locals())
            except Exception as e:
                print(e)
                put_success =False
                put_info = '发送失败'
                return render(req, 'file_trans.html', locals())
        else:
            return render(req, 'file_trans.html',locals())
    return render(req, 'file_trans.html', locals())
