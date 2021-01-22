from . import user
from flask import render_template, request, flash, session, redirect, url_for, json, make_response, jsonify
from app.models import Student
from ..utils import dict_to_obj


@user.route("/u_index")
def u_index():
    return render_template("/user/index/index.html")
    pass


@user.route("/info_detail")
def info_detail():

    return render_template("/user/info/info.html")
'''
peewee的查找方法不会反悔None，所以包装一下，查不到就返回None
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
