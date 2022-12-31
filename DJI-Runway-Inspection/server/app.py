import datetime
import json
import os
import cv2 as cv
import time
import traceback
from flask import jsonify, session, g
from flask import request
from flask_cors import *
from werkzeug.utils import secure_filename
import configs
from configs.log import logger
from modules.detect import detection
from modules.floder_analysis import add_prefix_files, contrast_floder
from modules import mainManager
from schema import models
from schema.models import app, db
from tools.tool import user_login_required
from concurrent.futures import ThreadPoolExecutor

# 获取当前文件的绝对路径
basedir = os.path.abspath(os.path.dirname(__file__))
executor = ThreadPoolExecutor()
CORS(app)

class API(object):
    def __init__(self):
        routes = [
            # 用户注册
            {'r': '/register', 'm': ['POST'], 'f': self.register},
            # 用户登录
            {'r': '/login', 'm': ['POST'], 'f': self.login},
            # 检查登录状态
            {'r': '/check_session', 'm': ['GET'], 'f': self.check_session},
            # 登出
            {'r': '/logout', 'm': ['DELETE'], 'f': self.logout},
            # 修改密码
            {'r': '/change_pwd', 'm': ['PUT'], 'f': self.change_pwd},
            # 主页
            {'r': '/', 'm': ['GET', 'POST'], 'f': self.home},
            # 接收图片json数据
            {'r': '/detectio', 'm': ['POST'], 'f': self.detectio},
            # 对比分析图片
            {'r': '/detectio_img', 'm': ['POST'], 'f': self.detectio_img},
            # 对比分析文件夹下的图片
            {'r': '/contrast_flod', 'm': ['GET'], 'f': self.contrast_flod},
            # 给前端返回分析结果
            {'r': '/floder_data', 'm': ['GET', 'POST'], 'f': self.floder_data},
            # 查看文件分析历史
            {'r': '/view_history', 'm': ['GET'], 'f': self.view_history},
            # 文件上传
            {'r': '/upload', 'm': ['POST'], 'f': self.upload},
            # 展示进度
            {'r': '/show_process', 'm': ['GET'], 'f': self.show_process},
        ]

        for route in routes:
            self.addroute(route)

    # 存储进度数据
    num_prcess = 0

    @staticmethod
    def addroute(route):
        app.add_url_rule(route['r'], view_func=route['f'], methods=route['m'])

    # 首页
    def home(self):
        return '<h1>Home</h1>'

    # 注册
    def register(self):
        req_dict = request.get_json()
        username = req_dict.get('username')
        password = req_dict.get('password')
        password1 = req_dict.get('password1')

        if not all([username, password, password1]):
            return jsonify(code=400, msg='参数不完整')
        if password != password1:
            return jsonify(code=401, msg='两次密码不一致')

        try:
            name = TbUser.query.filter_by(username=username).first()
            if name:
                return jsonify(code=400, msg='该用户已存在')
        except Exception as e:
            print(e)
            return jsonify(code=400, msg='数据库异常')

        user = TbUser(username=username, password=password,
                      create_time=time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())))
        try:
            db.session.add(user)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            print(e)
            return jsonify(code=400, msg='查询数据库异常')

        session["id"] = user.id
        session["username"] = username
        session["password"] = password

        return jsonify(code=200, msg="注册成功")

    # 登录
    def login(self):
        get_data = request.get_json()
        username = get_data.get("username")
        password = get_data.get("password")

        if not all([username, password]):
            return jsonify(code=400, msg="参数不完整")

        # 验证用户名密码
        user = TbUser.query.filter_by(username=username).first()
        if user and user.password == password:
            session["username"] = username
            session["id"] = user.id
            return jsonify(code=200, msg="登录成功")
        return jsonify(code=401, msg="账号或密码错误")

    # 检查登录状态
    def check_session(self):
        username = session.get("username")
        if username:
            return jsonify(username=username, code=200)
        return jsonify(code=400, msg="出错了,没登录")

    # 登出
    @user_login_required
    def logout(self):
        session.clear()
        return jsonify(msg="成功退出登录!", code=200)

    # 修改密码
    @user_login_required
    def change_pwd(self):
        uid = g.id
        req_dict = request.get_json()
        password = req_dict.get("password")
        new_password = req_dict.get("new_password")

        if not all([new_password, password, uid]):
            return jsonify(code=400, msg="参数不完整")

        try:
            user = TbUser.query.get(uid)
        except Exception as e:
            print(e)
            return jsonify(code=401, msg="获取用户信息失败")

        if user.status is False or user.password != password:
            return jsonify(code=402, msg="原密码密码错误")

        # 修改密码
        user.password = new_password
        try:
            db.session.add(user)
            db.session.commit()
            return jsonify(code=200, msg="修改密码成功!")
        except Exception as e:
            print(e)
            db.session.rollback()
            return jsonify(code=403, msg="修改密码失败,请稍后重试!")

    # 收到图片json参数
    def detectio(self):
        jsondata = request.get_json()
        # # 文件存放路径
        # file_path = jsondata.get('filepath')
        # # 原图
        # img_origin_name = jsondata.get('img_origin_name')
        # # 对比图
        # img_current_name = jsondata.get('img_current_name')
        try:
            # results = mainManager.receive_image_data(file_path, img_current_name, img_origin_name,configs.img_information['size'], configs.img_information['threshold'])
            results = mainManager.receive_image_data(jsondata)
            logger.info("处理图片成功")
            return jsonify({'statusCode': 200, 'msg': 'success', 'data': results})
        except Exception as e:
            logger.error(f"处理图片异常:{traceback.format_exc()}行数:{e.__traceback__.tb_lineno}")
            return jsonify({'statusCode': 500, 'msg': 'error', 'data': '图片处理失败'})

    # 对比分析图片
    def detectio_img(self):
        try:
            origin_image = request.files["origin_image"]
            current_image = request.files["current_image"]
            results = mainManager.receive_image(origin_image, current_image)
            logger.info("图片分析成功")

            tag, score, box, rectangle_img = detection(
                configs.img_information['img_path'] + configs.img_information['img_current_name'],
                configs.img_information['img_path'] + configs.img_information['img_origin_name'],
                size=configs.img_information['size'],
                threshold=configs.img_information['threshold'])

            if tag:
                filename = datetime.datetime.now().strftime("%Y%m%d%H%M%S") + ".JPG"
                file_path = "D:/images/out_img/"
                if not os.path.exists(file_path):
                    os.makedirs(file_path, 755)
                imgout_name = file_path + filename
                # 保存异物图片
                cv.imwrite(imgout_name, rectangle_img)
                logger.info("图片保存成功")
                my_host = "http:124.89.8.210:3006"
                url = my_host + "/images/out_img/" + filename
                data_list = []
                data_dic = {
                    "图片相似度得分": score,
                    "异物坐标": box,
                }
                data_list.append(data_dic)
                re = TbContrast(img1=origin_image.filename, img2=current_image.filename, tag=tag,
                                i_url=url, status=str(data_list),
                                create_time=time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())))
                db.session.add(re)
                db.session.commit()
                logger.info("文件保存到数据库成功")
            return jsonify({'statusCode': 200, 'msg': results})
        except Exception as e:
            logger.error(f"图片分析异常:{traceback.format_exc()}行数:{e.__traceback__.tb_lineno}")
            return jsonify({'code': -1, 'msg': 'error', 'data': '图片对比失败'})

    # 对比分析文件夹
    def contrast_flod(self):
        global path1
        file_path1 = "D:/images/write_imgs/"
        file_path2 = "D:/images/out_imgs/"
        lists = os.listdir(file_path1)
        lists.sort(key=lambda fn: os.path.getmtime(file_path1 + "\\" + fn))
        try:
            logger.info("开始执行对比文件夹下的文件...")
            floder1 = lists[-2]
            floder2 = lists[-1]
            path1 = file_path1 + floder1
            path2 = file_path1 + floder2
            out_path = file_path2 + floder1.replace("_a", "_c")
            if not os.path.exists(out_path):
                os.makedirs(out_path, 755)
            logger.info(path1)
            logger.info(path2)
            logger.info(out_path)
            add_prefix_files(path1)
            add_prefix_files(path2)
            for i in range(len(os.listdir(path1))):
                contrast_floder(path1, path2, out_path)
                num_process = i * 100 / len(os.listdir(path1))
                logger.info("文件夹图片对比分析成功...")
                return jsonify({"res": num_process})
        except Exception as e:
            logger.error(f"文件夹图片分析异常:{traceback.format_exc()}行数:{e.__traceback__.tb_lineno}")


    def show_process(self):
        global num_process
        return json.dumps(num_process)

    # def contrast_flod(self):
    #     executor.submit(self.floder_analysis)
    #     return jsonify({"statusCode": 200, "msg": "success"})

    # 给前端返回分析结果
    def floder_data(self):
        if request.method == 'GET':
            result = TbRunway.query.all()
            data_list = []
            for i in result:
                data_dic = {
                    "img1": i.img_name1,
                    "img2": i.img_name2,
                    "tag": i.tag,
                    "status": i.status,
                    "img_url": i.img_url,
                    "create_time": i.create_time
                }
                data_list.append(data_dic)
            return jsonify({'statusCode': 200, 'msg': 'success', "result": data_list})
        else:
            try:
                get_data = request.get_json()
                tag = get_data.get("tag")
                results = TbRunway.query.filter(TbRunway.tag == tag)
                data_list = []
                for i in results:
                    data_dic = {
                        "img1": i.img_name1,
                        "img2": i.img_name2,
                        "tag": i.tag,
                        "status": i.status,
                        "img_url": i.img_url,
                        "create_time": i.create_time
                    }
                    data_list.append(data_dic)
                    logger.info('图片分析结果为{}'.format(i))
                    logger.info('图片结果分析成功')
                return jsonify({'statusCode': 200, 'msg': 'success', "result": data_list})
            except Exception as e:
                logger.error(f"图片结果分析异常:{traceback.format_exc()}行数:{e.__traceback__.tb_lineno}")
                return jsonify({'statusCode': 500, 'msg': 'error', 'data': '图片结果分析失败'})

    # 查看历史
    def view_history(self):
        if request.method == 'GET':
            data_list = db.session.query(models.TbContrast).all()
            db.session.close()
            data_all = {}
            for item in data_list:
                data_dict = {
                    'image1': item.img1,
                    'image2': item.img2,
                    'tag': item.tag,
                    'i_url': item.i_url,
                    'status': item.status,
                    'create_time': item.create_time,
                }
                data_all[item.id] = data_dict
            return jsonify({'code': 200, 'msg': 'success', 'data': data_all})
        else:
            try:
                get_data = request.get_json()
                tag = get_data.get("tag")
                results = TbContrast.query.filter(TbContrast.tag == tag)
                data_list = []
                for i in results:
                    data_dic = {
                        "img1": i.img1,
                        "img2": i.img2,
                        "tag": i.tag,
                        "status": i.status,
                        "i_url": i.i_url,
                        "create_time": i.create_time
                    }
                    data_list.append(data_dic)
                    logger.info('图片分析结果为{}'.format(i))
                    logger.info('图片结果分析成功')
                return jsonify({'statusCode': 200, 'msg': 'success', "result": data_list})
            except Exception as e:
                logger.error(f"图片结果分析异常:{traceback.format_exc()}行数:{e.__traceback__.tb_lineno}")
                return jsonify({'statusCode': 500, 'msg': 'error', 'data': '图片结果分析失败'})

    # 文件上传
    def upload(self):
        try:
            file1 = request.files.getlist('file1')
            file2 = request.files.getlist('file2')
            if len(file1) != len(file2):
                logger.info('文件数量不一致,请重新输入')
            else:
                upload1_path = []
                upload2_path = []
                filename1_list = []
                filename2_list = []
                index = 1
                for filename1, filename2 in zip(file1, file2):
                    filename_1 = secure_filename(filename1.filename)
                    file_name1 = datetime.datetime.now().strftime("%Y%m%d%H%M%S") + "_a" + str(index) + "." + filename_1.rsplit('.', 1)[1]
                    file_path = "D:/images/write_imgs/" + datetime.datetime.now().strftime("%Y%m%d%H%M%S") + "_a" + "/"
                    if not os.path.exists(file_path):
                        logger.info("开始创建文件夹")
                        os.makedirs(file_path, 755)
                        logger.info("文件夹创建成功")
                    file1_path = file_path + file_name1
                    upload1_path.append(file1_path)
                    logger.info("upload1_path{}".format(upload1_path))
                    filename1.save(file1_path)
                    file_name2 = file_name1.replace("_a", "_b")
                    file_path2 = file_path.replace("_a", "_b")
                    if not os.path.exists(file_path2):
                        logger.info("开始创建文件夹")
                        os.makedirs(file_path2, 755)
                        logger.info("文件夹创建成功")
                    file2_path = file_path2 + file_name2
                    upload2_path.append(file2_path)
                    logger.info("upload2_path{}".format(upload2_path))
                    filename2.save(file2_path)
                    logger.info("文件上传成功")
                    filename1_list.append(file_name1)
                    filename2_list.append(file_name2)
                    index += 1
                logger.info("源文件保存成功")
            return jsonify({"statusCode": 200, "msg": "success", "data": (filename1_list ,filename2_list)})
        except Exception as e:
            logger.error(f"文件上传异常异常:{traceback.format_exc()}行数:{e.__traceback__.tb_lineno}")
            return jsonify({"statusCode": 500, "msg": "fail"})

    @staticmethod
    def start():
        app.run(host='0.0.0.0', port=5008, debug=False)


server = API()
logger.info('[+] AGX API is running [%s]' % datetime.datetime.now())

if __name__ == '__main__':
    server.start()
