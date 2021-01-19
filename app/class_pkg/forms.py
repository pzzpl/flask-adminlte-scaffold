from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, BooleanField, FileField, SelectField, TextAreaField, HiddenField
from wtforms.validators import DataRequired, Length, Email, Regexp, EqualTo
from app.models import Major


class ClassForm(FlaskForm):
    mjs = Major.select()
    class_name = StringField('班级名称', validators=[DataRequired(message='不能为空'), Length(0, 64, message='长度不正确')])
    # major = SelectField('班级专业', choices=[(v.id, v.major_name) for v in mjs],validators=[DataRequired(message='不能为空'), Length(0, 64, message='长度不正确')])
    submit = SubmitField('提交')