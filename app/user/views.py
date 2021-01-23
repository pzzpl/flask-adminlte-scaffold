from . import user
from flask import render_template, request, flash, session, redirect, url_for, json, make_response, jsonify
from app.models import Student,Numbertable,Alloc
from .. import utils, get_config
import base64

cfg = get_config()  # 获取全局配置文件
@user.route("/u_index")
def u_index():
    return render_template("/user/index/index.html")
    pass
def getStudentList(num):
    return  Student.select().where(Student.student_number == num)

'''
    http: // 172.26.167.195: 8888 /?hostname = 172.31.226.12 & username = root & password = b'aHBjbDY2MDE='
'''
def genertateURL(nb):
    webssh_host = cfg.WEBSSH_HOST
    webssh_port = cfg.WEBSSH_PORT
    container_host = nb.host
    container_port = nb.port
    encodestr = base64.b64encode(cfg.CONTAINER_PASSWORD.encode('utf-8'))
    encript_password = str(encodestr, 'utf-8')

    url = "http://" + webssh_host +":"+webssh_port+"/?hostname="+container_host+ "&port=" + container_port+ "&username=" + cfg.CONTAINER_USER + "&password="+encript_password
    return url
'''
视图函数步骤:
从session中查找student_number，再去查student的id
可能会用到多个id，去查db的分号情况.
在用分号的class_id去查资料和说明
把数据返回渲染
'''
@user.route("/info_detail")
def info_detail():
    student_number = session['user']
    student_list = getStudentList(student_number)
    #因为一个人可能同时在两个班，所以有可能有一个student_number对应多个student的id
    #所以把所有id查出来，一个个去找分号记录
    ids = []
    for row in student_list:
        ids.append(row)
    data = []
    for ele in ids:
        nbs = Numbertable.select().where(Numbertable.student_id == ele)
        for row in nbs: #每一条nb记录就是一个容器
            url = genertateURL(row) #生成webssh链接
            data.append(url)
            #根据nbs的allo_id查说明和资料  (to do)
            # Alloc.select().where(Alloc.id == row.alloc_id)





    return render_template("/user/info/info.html",data=data)
'''
peewee的查找方法不会返回None，所以包装一下，查不到就返回None
'''
def getStudent(num):
    try:
        return Student.select().where(Student.student_number == num).get()
    except:
        return None

@user.route("/u_login",methods=['POST'])
def u_login():

    rq_data = request.get_data()

    di = json.loads(rq_data)


    db_student = getStudent(di['student_number'])
    if db_student and di['student_psw'] == db_student.student_psw:
        session['user'] = di['student_number']
        response = make_response(jsonify({'msg': '登录成功'},200))
    else:
        response = make_response(jsonify({'msg': '账号不存在，或者密码错误.请找助教'},201))
    return response
