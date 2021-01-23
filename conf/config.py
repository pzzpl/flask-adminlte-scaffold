import os

basedir = os.path.abspath(os.path.dirname(__file__))


class Config:
    SECRET_KEY = 'stPkMpYjBvYF26UsrwxR898oyasgdbX853nOjShiIBZoCHzYKI76cpaRUzdU'
    DB_HOST = '127.0.0.1'
    DB_USER = 'root'
    DB_PASSWD = 'root'
    DB_DATABASE = 'data36'
    ITEMS_PER_PAGE = 10
    JWT_AUTH_URL_RULE = '/api/auth'
    DOWNLOAD_DIR = 'tpldir'
    #ssh相关
    # SSH_HOST = "172.31.226.159" #生产环境
    SSH_HOST = "172.31.226.12" #测试环境
    SSH_USER = "root"
    SSH_PWD = "hpcl6601"

    #生成webssh的host 和port
    WEBSSH_HOST = "172.31.225.136"
    WEBSSH_PORT= "8888"

    #容器账户名 密码
    CONTAINER_USER = "root"
    CONTAINER_PASSWORD = "szuxv6"


    #服务器批量创建容器的shell脚本名称xx.sh
    SCRIPT_NAME = "exec.sh"

    @staticmethod
    def init_app(app):
        pass


class DevelopmentConfig(Config):
    DEBUG = True


class TestingConfig(Config):
    TESTING = True


class ProductionConfig(Config):
    PRODUCTION = True


config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}
