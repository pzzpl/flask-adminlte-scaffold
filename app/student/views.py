from . import student
from .forms import StudentForm, UploadForm
from flask import render_template, request, flash, make_response, send_file, send_from_directory, redirect, url_for
from app import utils
from flask_login import login_required, current_user
from app.models import Student , Class,db,Major
import pandas as pd
import math
import os
from app import get_logger, get_config
def queryOneMajorByName(mj_name):
    try:
        val = Major().select().where(Major.major_name == mj_name).get()
    except:
        return None
    return val

cfg = get_config()  # 获取全局配置文件

@student.route('/student_add_form', methods=['GET', 'POST'])
def student_add_form():
    stf = StudentForm()
    if request.method == 'GET':  # 进入添加列表
        return render_template('/student/student_add.html', form=stf)
    if request.method == 'POST':  # 添加
        if stf.validate_on_submit():  # 数据验证正确
            data = Student()
            utils.form_to_model(stf, data)  # 把表单数据编程模型，导入库
            #print(data)
            data.save()
@student.route("/student_list",methods=['GET'])
@login_required
def student_list():
    # 接收参数 ,无就用默认
    page = int(request.args.get('page')) if request.args.get('page') else 1
    length = int(request.args.get('length')) if request.args.get('length') else cfg.ITEMS_PER_PAGE
    # 查询所有专业
    query = Student.select()
    total_count = query.count()
    # 处理分页
    if page: query = query.paginate(page, length)
    # for it in utils.query_to_list(query):
    #     print(it)
    dict = {'content': utils.query_to_list(query), 'total_count': total_count,
            'total_page': math.ceil(total_count / length), 'page': page, 'length': length}
    return render_template("/student/student_list.html", form=dict, current_user=current_user)
    pass
"""
lzp 2020-12-11
#这里用最笨的方法将excel表的学生信息，插入到数据库
    1.取excel表的5~最后一行，0~3列（因为第一列是下标，不要），形成一个dataframe
    3.先创建一个班级,后续要用来分号
    2.遍历dataframe的所有行，对于每一行，创建一个学生对象，一个专业对象，
    3.填好对象的值，调用pwee的API插入到数据库
#后续的优化思路：
    1.直接读取参数form的数据，而不用再次利用pd.read_excel('ufloder/'+form.file.data.filename)去读磁盘
    2.对于dataframe能有更好的操作方法,譬如先将数据整合，再调用peewee的批量API
附件：
    pandas官方API：https://pandas.pydata.org/pandas-docs/stable/reference/frame.html#indexing-iteration
"""

def create_from_form(form):
    df = pd.read_excel('ufloder/'+form.file.data.filename)
    # data = df.head()  # 默认读取前5行的数据
    data = df.iloc[5:,0:3]

    # print("获取到所有的值:\n{0}".format(data))  # 格式化输出
    data = data.rename(columns={'深圳大学研究生Linux操作系统点名册':'student_number', 'Unnamed: 1':'student_name','Unnamed: 2':'major_name'})
    # print("获取到所有的值:\n{0}".format(data))  # 格式化输出

    #开启事务
    with db.atomic() as tx:
        class_pkg = Class() #创建一个班级
        class_pkg.class_name = "计算机"+ str(Class.select().count()) + "班"
        class_pkg.save()

        i = 0
        while(i < len(data)):
            # print(data.iloc[i])
            obj = data.iloc[i]
            std = Student()
            std.student_name = obj['student_name']
            std.student_number = obj['student_number']
            std.student_psw = obj['student_number']
            #保存其专业
            mj = Major()
            mj.major_name = obj['major_name']

            '''
            # 由于查询不存在时，是抛出异常（菜！~~~）,另外写一个函数使得有异常时返回None
            '''
            mj_db = queryOneMajorByName(obj['major_name'])


            if(mj_db != None ): #已经有这个专业
                std.student_major = mj_db.id
            else: #没有这个专业，插入这个专业，然后保存到std中
                mj.save()
                std.student_major = mj.get_id()
            print(mj.get_id())

            std.student_class = class_pkg.get_id()
            #保存学生
            std.save()
            i+=1



@student.route('/upload/', methods=['POST', 'GET'])
@login_required
def upload():
    # 实例化表单
    form = UploadForm()
    if form.validate_on_submit():
        # 获取上传文件的文件名;
        filename = form.file.data.filename
        print(filename)
        # 将上传的文件保存到服务器;
        form.file.data.save('ufloder/' + filename)
        print(form.file.data)
        flash("上传成功", 'ok')
        create_from_form(form)
        return redirect(url_for("student.student_list"))
    return render_template('upload.html', form=form)

@student.route('/download',methods=['POST', 'GET'])
@login_required
def download():
    # print(app.instance_path)
    # dirpath = os.path.join(app.root_path, 'tpldir/')  # 这里是下在目录，从工程的根目录写起，比如你要下载static/js里面的js文件，这里就要写“static/js”
    # DOWNLOAD_DIR
    # UPLOAD_FOLDER = './info/modules/passport/{}.csv'.format(file_name)  # 第一种方法
    # ROOT_FOLDER = os.path.join(os.getcwd(), 'tpldir')  # 整合绝对路径
    # # cfg.DOWNLOAD_DIR
    # print(ROOT_FOLDER)
    # response = make_response(send_file('', mimetype='text/csv', attachment_filename='tpl.csv'))
    # return response
    # return '123'
    # return make_response(send_from_directory(directory='',filename='tpl.csv',as_attachment=True))
    ROOT_FOLDER = os.path.join(os.getcwd(), cfg.DOWNLOAD_DIR)  # 整合绝对路径
    # cfg.DOWNLOAD_DIR
    print(ROOT_FOLDER)
    return send_from_directory(ROOT_FOLDER,filename='tpl.xlsx',as_attachment=True)
