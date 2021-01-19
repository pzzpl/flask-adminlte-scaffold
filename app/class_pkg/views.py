from . import class_pkg
from app.class_pkg.forms import ClassForm
from flask import render_template, request, flash
from app import utils
import math
from flask_login import login_required, current_user
from flask_login import login_required
from app.models import Class
from app import get_logger, get_config
cfg = get_config()  # 获取全局配置文件
#添加班级
@class_pkg.route("/class_add_form", methods=['GET', 'POST'])
@login_required
def class_add_form():
    clf = ClassForm()
    if request.method == 'GET':  # 进入添加列表
        return render_template('/class/class_add.html', form=clf)
    if request.method == 'POST':  # 添加
        if clf.validate_on_submit():  # 数据验证正确
            data = Class()
            utils.form_to_model(clf, data)  # 把表单数据编程模型，导入库
            # print(data)
            data.save()
            flash("添加成功", 'ok')
            return render_template('/class/class_add.html', form=clf)
#班级列表
@class_pkg.route("/class_list",methods=['GET'])
def class_list():
    # 接收参数 ,无就用默认
    page = int(request.args.get('page')) if request.args.get('page') else 1
    length = int(request.args.get('length')) if request.args.get('length') else cfg.ITEMS_PER_PAGE
    # 查询所有专业
    query = Class.select()
    total_count = query.count()
    # 处理分页
    if page: query = query.paginate(page, length)
    for it in utils.query_to_list(query):
        print(it)
    dict = {'content': utils.query_to_list(query), 'total_count': total_count,
            'total_page': math.ceil(total_count / length), 'page': page, 'length': length}
    return render_template("/class/class_list.html", form=dict, current_user=current_user)
    pass