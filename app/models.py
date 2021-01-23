'''
author:lzp
date:2020-11-24
model类规范:命名使用下划线分割，例如镜像名称mirror_name.
model类的名称必须与数据库对应的列明相同
'''

from peewee import MySQLDatabase, Model, CharField, BooleanField, IntegerField,TextField,ForeignKeyField,DateTimeField
import json
from werkzeug.security import check_password_hash
from flask_login import UserMixin
from app import login_manager
from conf.config import config
import os

cfg = config[os.getenv('FLASK_CONFIG') or 'default']

db = MySQLDatabase(host=cfg.DB_HOST, user=cfg.DB_USER, passwd=cfg.DB_PASSWD, database=cfg.DB_DATABASE)


class BaseModel(Model):
    class Meta:
        database = db

    def __str__(self):
        r = {}
        for k in self._data.keys():
            try:
                r[k] = str(getattr(self, k))
            except:
                r[k] = json.dumps(getattr(self, k))
        # return str(r)
        return json.dumps(r, ensure_ascii=False)


# 管理员工号
class User(UserMixin, BaseModel):
    username = CharField()  # 用户名
    password = CharField()  # 密码
    fullname = CharField()  # 真实性名
    email = CharField()  # 邮箱
    phone = CharField()  # 电话
    status = BooleanField(default=True)  # 生效失效标识

    def verify_password(self, raw_password):
        print(raw_password)
        return check_password_hash(self.password, raw_password)
        #return True

# 通知人配置 （没有用的，不用管，也不要删。)
class CfgNotify(BaseModel):
    check_order = IntegerField()  # 排序
    notify_type = CharField()  # 通知类型：MAIL/SMS
    notify_name = CharField()  # 通知人姓名
    notify_number = CharField()  # 通知号码
    status = BooleanField(default=True)  # 生效失效标识
#专业
class Major(BaseModel):
    major_name = CharField() #专业名称
#班级
class Class(BaseModel):
    class_name = CharField() #班级名称
    # major = ForeignKeyField(Major,backref="classes") #班级外键



#学生
class Student(BaseModel):
    student_name = CharField() #学生名称
    student_number = CharField() #学生学号 登录号码
    student_sex = BooleanField() #学生性别
    student_email = CharField() # 学生邮箱
    #登录认证相关
    student_psw = CharField() #前端平台登录密码

    student_class = ForeignKeyField(Class,backref="students") #班级外键
    student_major = ForeignKeyField(Major,backref="students") #专业外键

    status = BooleanField(default=True)  # 生效标识

    #密码加密
    def verify_password(self, raw_password):
        print(raw_password)
        return check_password_hash(self.student_psw, raw_password)

#镜像
class Mirror(BaseModel):
    mirror_repository = CharField() #镜像名称
    mirror_createtime = DateTimeField() #镜像的创建时间(系统扫描到的时间
    docker_image_id = CharField() #镜像的id（在docker中的

#容器
class Container(BaseModel):
    container_name = CharField() #容器名称
    student = ForeignKeyField(Student,backref="containers")
    container_port1 = CharField() #端口映射1
    container_port2 = CharField()  # 端口映射2
    container_port3 = CharField()  # 端口映射3
    container_port4 = CharField()  # 端口映射4

    container_desc = CharField() #容器的描述
class Alloc(BaseModel):
    '''
        added by lzp 2020-1-23 用于扩展容器使用说明
    '''
    specification = CharField()  # 容器使用说明
    file_name = CharField()  # 文件路径名称
    class_id = ForeignKeyField(Class,backref="allocs")
#分号表
class Numbertable(BaseModel):
    port = CharField() #port
    host = CharField() #host
    student_id = ForeignKeyField(Student,backref="ports") #stu_id
    alloc_id = ForeignKeyField(Alloc,backref="containers") # 分号所属的班级

#实验课程
class Course(BaseModel):
    course_title = CharField() #课程名称
    course_starttime = DateTimeField() #实验课开始时间
    course_endtime = DateTimeField() #实验结束时间
    # teacher = ForeignKeyField(Teacher,backref="courses") #实验课的任课老师
    docker = ForeignKeyField(Mirror,backref="courses")

#课程-学生中间表
class SC(BaseModel):
    student = ForeignKeyField(Student,backref="courses")
    course = ForeignKeyField(Course,backref="students")

@login_manager.user_loader
def load_user(user_id):
    return User.get(User.id == int(user_id))

# 建表
def create_table():
    db.connect()
    db.create_tables([User,Class,Major,Student,Numbertable,Alloc])





if __name__ == '__main__':
    create_table()
