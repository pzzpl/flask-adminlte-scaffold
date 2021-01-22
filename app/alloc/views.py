from app import get_logger, get_config
from .forms import AllocForm
from app import utils
from . import alloc
import paramiko
from io import StringIO
from flask import render_template, request, flash, make_response, send_file, send_from_directory, url_for, redirect
from app.models import Class, Student, Numbertable
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


def exe_cmd(cmd):
    ssh = getSSH()
    stdin, stdout, stderr = ssh.exec_command(cmd)
    exe_result = stdout.read().decode()
    error_info = stderr.read().decode()
    print(error_info)
    ssh.close()
    return exe_result


def ssh2image():
    # ssh = getSSH()
    # stdin, stdout, stderr = ssh.exec_command('docker images')
    # images_info = stdout.read().decode()
    # ssh.close()
    images_info = exe_cmd('docker images')

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


'''
分号第一步：确定镜像id
分号第二步：确定分给哪个班级，和分哪些端口号
下面这个是分号的shell脚本:
str=Linux_
for ((i= 0; i < ${1}; i=i+1))
do
	docker run --restart always -itd  --name ${str}${i} -p $((${i}+$(2))):22  $(3)
	sleep 1
done

执行脚本的命令：其中有3个参数
第一个：强制为0
第二个：分配多少个容器
第三个：分配端口号的base号
第四个：image的ID
执行例子：
./exec.sh  55 20000 wd2339204
'''


@alloc.route("/alloc_first", methods=['GET', 'POST'])
def alloc_first():


    image_info = ssh2image()  # 获取镜像信息

    # print(image_info)
    data = {
        "image_info": image_info,
        "class_info": utils.query_to_list(Class.select())
    }
    if(len(image_info) == 0) :
        flash("服务器网络可能出问题，或者是docker出问题了，请您去看看")
    return render_template("/allocation/alloc_info.html", data=data)


def dumpStu2Port(baseport , class_id,query):

    # students = utils.query_to_list(query)
    port_cnt = int(baseport)
    for row in query:
        nb = Numbertable()
        nb.student_id = row.id
        nb.host = cfg.SSH_HOST
        nb.port = str(port_cnt)
        port_cnt += 1
        nb.save()



@alloc.route("/alloc_second", methods=['POST'])
def alloc_second():
    # 先获取所需分配的班级的人数、端口base号、镜像id
    cid = request.form["class_id"]
    query = Student.select()
    total_count = query.count() #班级人数
    # total_count = 2  # 测试用

    img_id = request.form['image_id']

    protbase = request.form['portbase']

    # 组件命令
    script_name = cfg.SCRIPT_NAME  # 获取脚本名称
    cmd = "./" + script_name + " " + "0 " + str(total_count) + " " + str(protbase) + " " + img_id
    print(cmd)
    res = exe_cmd(cmd)
    print(res)

    # 获得脚本的执行结果，判断是否执行成功。
    # 如果执行成功 ：就从base号开始--->一个个分配给班里面的人，并记录到数据库
    row_list = res.split("\n")
    if(len(row_list ) - 1  == total_count):
        flash("分配成功")
        # 下面是创建成功
        dumpStu2Port(protbase, cid, query)
    else:
        flash("分配失败")
    #展示 分配情况
    return redirect(url_for("alloc.alloc_first"))
