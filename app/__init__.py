from flask import Flask
from flask_login import LoginManager
from conf.config import config
import logging
from logging.config import fileConfig
import os

login_manager = LoginManager()
login_manager.session_protection = 'strong'
login_manager.login_view = 'auth.login'

fileConfig('conf/log-app.conf')

def get_logger(name):
    return logging.getLogger(name)


def get_basedir():
    return os.path.abspath(os.path.dirname(__file__))


def get_config():
    return config[os.getenv('FLASK_CONFIG') or 'default']


def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)

    login_manager.init_app(app)
    #注册蓝图
    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    from .auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint)
    #注册mirror蓝图  2020-11-24
    from  .mirror import  mirror as mirror_blueprint
    app.register_blueprint(mirror_blueprint)
    #注册学生蓝图
    from  .student import  student as student_blueprint
    app.register_blueprint(student_blueprint)

    #注册major蓝图
    from .major  import  major as major_blueprint
    app.register_blueprint(major_blueprint)

    return app
