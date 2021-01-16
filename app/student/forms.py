from flask_wtf import FlaskForm
from flask_wtf.file import FileRequired, FileAllowed
from wtforms import StringField, SubmitField, BooleanField, FileField, SelectField, TextAreaField, HiddenField
from wtforms.validators import DataRequired, Length, Email, Regexp, EqualTo
from app.models import Class


class StudentForm(FlaskForm):
    # class_choices = []  # 先所有的班级查出来，再放进去form，传给前端
    #
    # def __init__(self):
    #     t = Class.select()
    #     for c in t:
    #         self.class_choices.append(c.id)
    cl = Class.select()
    student_name = StringField('学生姓名', validators=[DataRequired(message='不能为空'), Length(0, 64, message='长度不正确')])
    student_number = StringField('学号', validators=[DataRequired(message='不能为空'), Length(0, 64, message='长度不正确')])
    student_sex = SelectField('性别', choices=[(1, '男'), (0, '女')],
                              validators=[DataRequired(message='不能为空'), Length(0, 64, message='长度不正确')])
    student_email = StringField('邮箱')
    student_psw = StringField('密码', default='111111')
    student_class = SelectField('班级', choices=[(v.id, v.class_name) for v in cl],
                                validators=[DataRequired(message='不能为空'), Length(0, 64, message='长度不正确')])
    status = BooleanField('生效标识', default=True)
    submit = SubmitField('提交')


class UploadForm(FlaskForm):
    """用户上传文件的表单"""
    file = FileField(
        label="请上传表格",
        validators=[
            # 文件必须选择;
            FileRequired(),
            # 指定文件上传的格式;
            FileAllowed(['xlsx'], '只接收.xlsx格式的文件')
        ]
    )
    submit = SubmitField(
        render_kw={
            'value': "上传",
            'class': 'btn btn-success pull-right'
        }
    )
