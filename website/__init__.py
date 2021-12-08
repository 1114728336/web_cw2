from logging.handlers import RotatingFileHandler

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from os import path
from flask_login import LoginManager
import logging

db = SQLAlchemy()
DB_NAME = "database.db"


def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = "helloworld"
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'
    db.init_app(app)
    from .auth import auth
    from .views import views
    logging.basicConfig(level=logging.DEBUG)
    # 创建日志记录器，指明日志保存的路径，每个日志文件的最大值，保存的日志文件个数上限
    log_handle = RotatingFileHandler("log.txt", maxBytes=1024 * 1024, backupCount=5)
    # 创建日志记录的格式
    formatter = logging.Formatter("format = '%(asctime)s - %(name)s - %(levelname)s - %(message)s-%(funcName)s',")
    # 为创建的日志记录器设置日志记录格式
    log_handle.setFormatter(formatter)
    # 为全局的日志工具对象添加日志记录器
    logging.getLogger().addHandler(log_handle)
    logging.warning('Warning message')
    logging.error('Error message')
    logging.critical('Failed message')
    app.register_blueprint(views, url_prefix="/")
    app.register_blueprint(auth, url_prefix="/")

    from .models import User, Comment, Post, Like

    create_database(app)

    login_manager = LoginManager()
    login_manager.login_view = "auth.login"
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id))

    return app


def create_database(app):
    if not path.exists("website/" + DB_NAME):
        db.create_all(app=app)
        print("Created database!")
