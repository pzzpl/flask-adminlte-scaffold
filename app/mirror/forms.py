from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Length


class MirrorForm(FlaskForm):
    mirror_address = StringField('镜像地址', validators=[DataRequired(message='不能为空'), Length(0, 64, message='长度不正确')])
    mirrir_name = StringField('镜像名称', validators=[DataRequired(message='不能为空'), Length(0, 64, message='长度不正确')])
    status = BooleanField('镜像状态', default=True)
    submit = SubmitField('提交')
