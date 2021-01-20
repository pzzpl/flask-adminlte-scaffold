from flask_wtf import FlaskForm
from flask_wtf.file import FileRequired, FileAllowed
from wtforms import StringField, SubmitField, BooleanField, FileField, SelectField, TextAreaField, HiddenField
from wtforms.validators import DataRequired, Length, Email, Regexp, EqualTo
from app.models import Class


class AllocForm(FlaskForm):
    cl = Class.select()
    class_name = SelectField('班级', choices=[(v.id, v.class_name) for v in cl],
                                validators=[DataRequired(message='不能为空')])
    submit = SubmitField('nexy')