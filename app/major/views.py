from . import major
from app import get_logger, get_config
import math
from flask_login import login_required, current_user
from .forms import MajorForm
from flask import render_template, request, flash, redirect
from app import utils
from app.models import Major


cfg = get_config() #获取全局配置文件
'''
添加专业
'''
@major.route("/major_add_form",methods=['GET', 'post'])
@login_required
def major_add_form():
    mjf = MajorForm()
    if request.method == 'GET':  # 进入添加列表
        return render_template('/major/major_add.html', form=mjf)
    if request.method == 'POST':  # 添加
        if mjf.validate_on_submit():  # 数据验证正确
            data = Major()
            utils.form_to_model(mjf, data)  # 把表单数据编程模型，导入库
            #print(data)
            data.save()
            flash("添加成功", 'ok')
            return render_template('/major/major_add.html', form=mjf)

'''
专业列表
'''
@major.route("/major_list",methods=['GET', 'post'])
@login_required
def major_list():
    # 接收参数 ,无就用默认
    page = int(request.args.get('page')) if request.args.get('page') else 1
    length = int(request.args.get('length')) if request.args.get('length') else cfg.ITEMS_PER_PAGE
    #查询所有专业
    query = Major.select()
    total_count = query.count()
    #处理分页
    if page: query = query.paginate(page, length)
    # for it in utils.query_to_list(query):
    #     print(it)
    dict = {'content': utils.query_to_list(query), 'total_count': total_count,
            'total_page': math.ceil(total_count / length), 'page': page, 'length': length}
    return render_template("/major/major_list.html", form=dict, current_user=current_user)

@major.route('/major/search/<string:criteria>',methods=['GET'])
@login_required
def searchMajor(criteria):
    # print(criteria)
    query = Major.select().where(Major.major_name.contains(criteria))
    total_count = query.count()
    # 使用默认分页
    page = 1
    length = cfg.ITEMS_PER_PAGE
    #处理分页
    if page: query = query.paginate(page, length)
    for it in utils.query_to_list(query):
        print(it)
    dict = {'content': utils.query_to_list(query), 'total_count': total_count,
            'total_page': math.ceil(total_count / length), 'page': page, 'length': length}
    # return render_template("/major/major_list.html", form=dict, current_user=current_user)
    return render_template("/major/refresh_table.html", form=dict, current_user=current_user)