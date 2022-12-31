# coding: utf-8
from flask_sqlalchemy import SQLAlchemy
from flask import Flask

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root:Ytwl@2022!@127.0.0.1:3306/db_runway'
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SECRET_KEY"] = "jjjsks"
db = SQLAlchemy(app)  # 实例化的数据库


# 航线表
class TbRoute(db.Model):
    __tablename__ = 'tb_route'
    id = db.Column(db.Integer, primary_key=True, comment='主键')
    route_name = db.Column(db.String(255), nullable=False, comment='航线名称')
    tasks = db.relationship("TbTask", backref="tb_route")
    create_time = db.Column(db.DateTime, nullable=False, comment='创建时间')


# 任务表
class TbTask(db.Model):
    __tablename__ = 'tb_task'
    id = db.Column(db.Integer, primary_key=True, comment='主键')
    task_name = db.Column(db.String(255), nullable=False, comment='任务名称')
    route_name = db.Column(db.String(255), nullable=False, comment='航线名称')
    is_analysis = db.Column(db.String(255), nullable=False, default='0', comment='是否已对比,0未对比,1为已完成,2为对比中')
    task_process = db.Column(db.String(255), nullable=False, comment='对比进度')
    is_orimg = db.Column(db.String(255), nullable=False, default='0', comment='是否为原图')
    route_id = db.Column(db.Integer, db.ForeignKey("tb_route.id"), comment='航线id')  # 所属航线
    tag = db.Column(db.String(255), default='0', nullable=False, comment='是否存在异物')
    imgs = db.relationship("TbImg", backref="tb_task")
    analysis = db.relationship("TbAnalysis", backref="tb_task")
    backup1 = db.Column(db.String(255), default='0', comment='备用字段1')
    backup2 = db.Column(db.String(255), default='0', comment='备用字段2')
    backup3 = db.Column(db.String(255), default='0', comment='备用字段3')
    backup4 = db.Column(db.String(255), default='0', comment='备用字段4')
    create_time = db.Column(db.DateTime, nullable=False, comment='创建时间')


# 图片表
class TbImg(db.Model):
    __tablename__ = 'tb_img'
    id = db.Column(db.Integer, primary_key=True, comment='主键')
    img_name = db.Column(db.String(255), nullable=False, comment='图片名')
    img_url = db.Column(db.String(255), nullable=False, comment='图片地址')
    is_analysis = db.Column(db.String(255), nullable=False, default='0', comment='是否已对比')
    task_id = db.Column(db.Integer, db.ForeignKey("tb_task.id"), comment='任务id')  # 所属任务
    backup1 = db.Column(db.String(255), default='0', comment='备用字段1')
    backup2 = db.Column(db.String(255), default='0', comment='备用字段2')
    backup3 = db.Column(db.String(255), default='0', comment='备用字段3')
    backup4 = db.Column(db.String(255), default='0', comment='备用字段4')
    create_time = db.Column(db.DateTime, nullable=False, comment='创建时间')


# 对比表
class TbAnalysis(db.Model):
    __tablename__ = 'tb_analysis'
    id = db.Column(db.Integer, primary_key=True, comment='主键')
    tag = db.Column(db.String(255), nullable=False, comment='是否存在异物')
    score = db.Column(db.String(255), comment='相似度得分')
    box = db.Column(db.String(255), comment='异物坐标')
    img_name = db.Column(db.String(255), comment='异物图名称')
    img_url = db.Column(db.String(255), comment='异物图地址')
    task_id = db.Column(db.Integer, db.ForeignKey("tb_task.id"), comment='任务id')  # 所属任务
    backup1 = db.Column(db.String(255), default='0', comment='备用字段1')
    backup2 = db.Column(db.String(255), default='0', comment='备用字段2')
    backup3 = db.Column(db.String(255), default='0', comment='备用字段3')
    backup4 = db.Column(db.String(255), default='0', comment='备用字段4')
    create_time = db.Column(db.DateTime, nullable=False, comment='创建时间')


db.create_all()

# class TbUser(db.Model):
#     __tablename__ = 'tb_user'
#
#     id = db.Column(db.Integer, primary_key=True, comment='主键')
#     username = db.Column(db.String(255), nullable=False, comment='用户名')
#     password = db.Column(db.String(255), nullable=False, comment='密码')
#     status = db.Column(db.Boolean, nullable=False, default=True)  # 真假代表正常异常状态
#     create_time = db.Column(db.DateTime, nullable=False, comment='注册时间')
#     update_time = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now)  # 最近一次登录时间
