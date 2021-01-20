from app import get_logger, get_config
from .forms import AllocForm
from . import alloc
import paramiko
from io import StringIO
from flask import render_template, request, flash, make_response, send_file, send_from_directory
import pandas as pd

cfg = get_config()  # 获取全局配置文件

'''
优化：可以变成ssh池，从里面获取连接，就不用每次都申请和关闭
'''


def getSSH():
    ssh_host_name = cfg.SSH_HOST
    ssh_user = cfg.SSH_USER
    ssh_pwd = cfg.SSH_PWD
    # 建立一个sshclient对象
    ssh = paramiko.SSHClient()
    # 允许将信任的主机自动加入到host_allow 列表，此方法必须放在connect方法的前面
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    # 调用connect方法连接服务器
    ssh.connect(hostname=ssh_host_name, port=22, username=ssh_user, password=ssh_pwd)
    return ssh


'''
通过sshclient，建立连接，发送查看docker所有images的命令，
返回命令结果
包装到页面
'''


def ssh2image():
    ssh = getSSH()
    stdin, stdout, stderr = ssh.exec_command('docker images')
    images_info = stdout.read().decode()
    ssh.close()

# print(images_info)
    # 以下代码解释命令结果
    row_list = images_info.split("\n")  # 按换行分割，返回list

    data = []
    for row in row_list[1:]:
        if (row != ''):
            row_split = list(filter(lambda x: x != '', row.split(" ")))  # 每一行按空格分，返回list
            data.append({"image_name": row_split[0], "image_id": row_split[2]})
    # ---------------------------
    return data


@alloc.route("/alloc_first", methods=['GET', 'POST'])
def alloc_first():
    image_info = ssh2image()  # 获取镜像信息
# print(image_info)
    return render_template("/allocation/allocation.html",data= image_info)


@alloc.route("/alloc_second/<string:image_id>", methods=['GET'])
def alloc_second(image_id):

    print(image_id)
    pass
