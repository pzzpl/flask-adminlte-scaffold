from . import student
from .forms import StudentForm, UploadForm
from flask import render_template, request, flash, redirect
from app import utils
from app.models import Student
import pandas as pd
import  xlrd


@student.route('/student_add_form', methods=['GET', 'post'])
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
"""
lzp 2020-12-11
返回值：返回的是学生model对象 列表
#to do 本方法没有提取form中的数据。而是直接读取磁盘上的文件，可能会造成时间的代价。
    后续优化
操作： 用pandas读取excel
       然后使用pandas工具读取前两列的dataframe，再转换成list，并且返回 
"""
def create_from_form(form):
    df = pd.read_excel('ufloder/'+form.file.data.filename)
    # data = df.head()  # 默认读取前5行的数据
    data = df.iloc[5:,0:3]

    # print("获取到所有的值:\n{0}".format(data))  # 格式化输出
    data = data.rename(columns={'深圳大学研究生Linux操作系统点名册':'student_number', 'Unnamed: 1':'student_name','Unnamed: 2':'major_name'})


    pass
@student.route('/upload/', methods=['POST', 'GET'])
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
        student_data = create_from_form(form)
        return render_template('/upload_data_List.html/',form = student_data) #跳到上传列表展示页面
    return render_template('upload.html', form=form)