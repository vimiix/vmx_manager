#coding=utf-8

import paramiko

class Remote(object):
    def __init__(self, host, username, password, port=22):
        self.host = host
        self.port = port
        self.username = username
        self.password = password

    def ssh(self, cmd):
        self.cmd = cmd
        try:
            #对远程服务做判断，如果远程失败，返回False
            trans = paramiko.Transport((self.host, self.port))
            trans.connect(username=self.username, password=self.password)
        except Exception as e:
            print e
            return False
        else:
            ssh = paramiko.SSHClient()
            ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            ssh._transport = trans
            stdin, stdout,stderr = ssh.exec_command(self.cmd)
            result = stdout.readlines()
            trans.close()
            return result

class Sftp(object):
    def __init__(self,hostip,username,passwd,port=22):  #初始化主机，用户名，密码，端口号
        self.hostip = hostip
        self.port = port
        self.username = username
        self.passwd = passwd

    def ssh(self):
        try:
            self.transport = paramiko.Transport((self.hostip, self.port))
            self.transport.connect(username=self.username, password=self.passwd)
        except Exception as e:
            return False
        else:
            return True

    def put(self,upload_file,remote_path='/tmp/'):
        self.upload_file = upload_file.replace('\\','/')
        self.remote_path = remote_path+upload_file.split('\\')[-1]

        #基于用户名密码文件分发
        if self.ssh():
            sftp = paramiko.SFTPClient.from_transport(self.transport)
            sftp.put(self.upload_file, self.remote_path)
            self.transport.close()

    def get(self,getfile,savepath):
        self.getfile = getfile
        self.savepath = savepath

        #基于用户名密码文件获取
        if self.ssh():
            sftp = paramiko.SFTPClient.from_transport(self.transport)
            # 将remove_path 下载到本地 local_path
            sftp.get(self.getfile, self.savepath)
            self.transport.close()


