from . import mirror
from flask import render_template
from .forms import MirrorForm
from app import  utils
from app.models import  Mirror
'''
author:lzp
date:2020-11-24
带wtf_from跳转到mirroredit页面
'''
@mirror.route('/mirroredit', methods=['GET','POST'])
def mirroredit():
    form = MirrorForm()
    if form.validate_on_submit():
        print(form)
        model = Mirror()
        utils.form_to_model(model,form)
        model.save()


    return render_template('mirror/mirroredit.html', form=form)
