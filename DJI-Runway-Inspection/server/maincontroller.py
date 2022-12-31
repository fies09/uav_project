import datetime
import os
import traceback
import oss2
import configs
from modules.floder_analysis import auto_compare, contrast_floder
from concurrent.futures import ThreadPoolExecutor
from flask import jsonify
from flask import request
from flask_cors import CORS
from configs.log import logger
from schema.models import app, TbTask, TbAnalysis, TbRoute, db, TbImg
from threading import Thread
from tools.sql_operations import insert_route, insert_task, insert_img

# 获取当前文件的绝对路径
basedir = os.path.abspath(os.path.dirname(__file__))
executor = ThreadPoolExecutor()
CORS(app)

class API(object):
    def __init__(self):
        routes = [
            # 返回航线列表
            {'r': '/show_route', 'm': ['GET'], 'f': self.show_route},  #
            # 返回任务列表
            {'r': '/show_task/<rid>/', 'm': ['GET'], 'f': self.show_task},  #
            # 对比分析文件夹下的图片
            {'r': '/contrast_data', 'm': ['POST'], 'f': self.contrast_data},  #
            # 根据任务ID查询任务图片
            {'r': '/img_for_task/<tid>/', 'm': ['GET'], 'f': self.img_for_task},  #
            # 根据任务ID查看该任务已完成对比的图片
            {'r': '/over_img', 'm': ['POST'], 'f': self.over_img},  #
            # 查看对比历史
            {'r': '/analysis_history', 'm': ['GET', 'POST'], 'f': self.analysis_history},  #
            # 指定原图接口
            {'r': '/specify_original', 'm': ['POST'], 'f': self.specify_original},  #
            # 下载接口
            {'r': '/download_file', 'm': ['POST'], 'f': self.download_file},  #
        ]
        for route in routes:
            self.addroute(route)

    @staticmethod
    def addroute(route):
        app.add_url_rule(route['r'], view_func=route['f'], methods=route['m'])

    # 下载接口
    def download_file(self):
        try:
            get_data = request.get_json()
            logger.info(">>>>>>>>>>>>>>>>>>收到下载消息: {}".format(get_data))
            # 原文件名(文件名)
            fname = get_data.get('fname')
            # 原始文件夹名(任务名)
            floder_name = get_data.get('fpath')
            # 完整路径(阿里云文件路径)
            fpath = get_data.get('fnpath')
            # bucket名
            bucket_name = get_data.get("bucket")
            auth = oss2.Auth(configs.oss_config['accesskey_id'], configs.oss_config['accesskey_secret'])
            bucket = oss2.Bucket(auth, 'https://oss-cn-beijing.aliyuncs.com', bucket_name)
            path = "D:/images/write_imgs/"
            file_path = path + str(floder_name)
            if not os.path.exists(file_path):
                os.makedirs(file_path, 755)
            logger.info("开始下载文件: {}".format(fname))
            bucket.get_object_to_file(fpath, file_path + '/' + fname)
            logger.info("{}下载成功".format(fname))
            # 航线数据写入
            insert_route(floder_name)
            # 任务数据写入
            insert_task(floder_name)
            # 向图片表插入数据
            insert_img(fname, floder_name)
            out_path = "D:/images/out_imgs/" + floder_name + "/"
            if not os.path.exists(out_path):
                os.makedirs(out_path, 755)
            result = TbTask.query.filter(TbTask.is_orimg == "1")
            if result:
                for res in result:
                    path1 = path + res.task_name
                    path2 = file_path
                    logger.info("out_path1:{}".format(out_path))
                    if path1.split("_")[-1] == path2.split("_")[-1]:
                        logger.info("开始修改对比状态")
                        try:
                            db.session.query(TbTask).filter(TbTask.task_name == floder_name).update({"is_analysis": "2"})
                            db.session.commit()
                        except Exception as e:
                            logger.error(f"自动对比状态修改失败:{traceback.format_exc()}行数:{e.__traceback__.tb_lineno}")
                            db.session.rollback()
                        logger.info("自动对比状态修改成功")
                        # 实现自动对比功能
                        logger.info('开始执行自动对比功能')
                        Thread(target=auto_compare, args=(path1, file_path, fname, out_path)).start()
                        logger.info('自动对比成功!')
                        # 判断任务是否为有异物的任务
                        try:
                            db.session.query(TbTask).filter(TbTask.task_name == floder_name).update({"tag": "1"})
                            db.session.commit()
                        except Exception as e:
                            logger.error(f"自动对比异物状态修改失败:{traceback.format_exc()}行数:{e.__traceback__.tb_lineno}")
                            db.session.rollback()
                        logger.info("异物状态修改成功")
                        # 修改图片对比状态
                        try:
                            db.session.query(TbImg).filter(TbImg.img_name == fname).update({"is_analysis": "1"})
                            db.session.commit()
                        except Exception as e:
                            logger.error(f"自动对比状态修改失败:{traceback.format_exc()}行数:{e.__traceback__.tb_lineno}")
                            db.session.rollback()
                        logger.info("图片自动对比状态修改成功")
                    else:
                        return jsonify({"code": 501, "msg": "未在同一航线下,请重新选择"})
                    return jsonify({"code": 200, "msg": "对比成功！"})
            else:
                return jsonify({"code": 502, "msg": "未设置原图模板,请先设置原图模板"})
            return jsonify({"code": 200, "msg": "首次下载成功！"})
        except Exception as e:
            logger.error(f"自动对比图片分析异常:{traceback.format_exc()}行数:{e.__traceback__.tb_lineno}")
            return jsonify({'code': 404, 'msg': 'error', 'data': '数据详情返回出错！'})

    # 返回航线列表
    def show_route(self):
        obj_route = TbRoute.query.all()
        route_list = []
        for route in obj_route:
            dict_route = {
                "id": route.id,
                "route_name": route.route_name,
                "create_time": str(route.create_time)
            }
            route_list.append(dict_route)
        return jsonify({"statusCode": 200, "msg": "success", "data": route_list})

    # 根据航线ID查询任务列表
    def show_task(self, rid):
        try:
            task_list = []
            obj_task = TbTask.query.filter(TbTask.route_id == rid)
            for i in obj_task:
                dict_task = {
                    "id": i.id,
                    "task_name": i.task_name,
                    "route_id": i.route_id,
                    "route_name": i.route_name,
                    "is_analysis": i.is_analysis,
                    "task_process": i.task_process,
                    "tag": i.tag,
                    "is_orimg": i.is_orimg,
                    "create_time": str(i.create_time),
                }
                task_list.append(dict_task)
            return jsonify({"statusCode": 200, "msg": "success", "data": task_list})
        except Exception as e:
            logger.error(f"根据航线id查询任务列表异常:{traceback.format_exc()}行数:{e.__traceback__.tb_lineno}")
            return jsonify({'statusCode': 500, 'msg': 'fail'})

    # 根据任务ID查询任务图片
    def img_for_task(self, tid):
        try:
            ltask_details = []
            obj_task = TbImg.query.filter(TbImg.task_id == tid)
            for re_i in obj_task:
                dict_task = {
                    'id': re_i.id,
                    'img_name': re_i.img_name,
                    'img_url': re_i.img_url,
                    'is_analysis': re_i.is_analysis,
                    'create_time': str(re_i.create_time),
                }
                ltask_details.append(dict_task)
            return jsonify({'statusCode': 200, 'msg': 'success', 'data': ltask_details})
        except Exception as e:
            logger.error(f"根据任务ID查询任务图片异常:{traceback.format_exc()}行数:{e.__traceback__.tb_lineno}")
            return jsonify({'statusCode': 500, 'msg': '获取任务{}下图片失败!'.format(tid)})

    # 根据任务ID查看已对比完图片
    def over_img(self):
        get_data = request.get_json()
        taskid = get_data.get("taskid")
        try:
            over_list = []
            obj_over = TbAnalysis.query.filter(TbAnalysis.task_id == taskid)
            for over in obj_over:
                dict_task = {
                    'id': over.id,
                    'tag': over.tag,
                    'score': over.score,
                    'box': over.box,
                    'img_name': over.img_name,
                    'img_url': over.img_url,
                    'task_id': over.task_id,
                    'create_time': str(over.create_time),
                }
                over_list.append(dict_task)
            return jsonify({'statusCode': 200, 'msg': 'success', 'result': over_list})
        except Exception as e:
            logger.error(f"根据任务ID查看已对比完图片异常:{traceback.format_exc()}行数:{e.__traceback__.tb_lineno}")
            return jsonify({'statusCode': 500, 'msg': '获取任务{}下已对比完成图片失败!'.format(taskid)})

    # 查看对比历史记录
    def analysis_history(self):
        if request.method == 'GET':
            results = TbAnalysis.query.all()
            data_list = []
            for result in results:
                data_dic = {
                    "tag": result.tag,
                    "score": result.score,
                    "img_name": result.img_name,
                    "img_url": result.img_url,
                    "task_id": result.task_id,
                    "create_time": str(result.create_time)
                }
                data_list.append(data_dic)
                logger.info('图片分析结果为{}'.format(result))
                logger.info('图片结果分析成功')
            return jsonify({'statusCode': 200, 'msg': 'success', "result": data_list})
        else:
            try:
                get_data = request.get_json()
                aid = get_data.get("id")
                results = TbAnalysis.query.filter(TbAnalysis.id == aid)
                data_list = []
                for result in results:
                    data_dic = {
                        "tag": result.tag,
                        "score": result.score,
                        "img_name": result.img_name,
                        "img_url": result.img_url,
                        "task_id": result.task_id,
                        "create_time": str(result.create_time)
                    }
                    data_list.append(data_dic)
                    logger.info('图片分析结果为{}'.format(result))
                    logger.info('图片结果分析成功')
                return jsonify({'statusCode': 200, 'msg': 'success', "result": data_list})
            except Exception as e:
                logger.error(f"查看对比历史记录异常:{traceback.format_exc()}行数:{e.__traceback__.tb_lineno}")
                return jsonify({'statusCode': 500, 'msg': 'error', 'data': '图片结果分析失败'})

    # 指定原图模板
    def specify_original(self):
        try:
            get_data = request.get_json()
            specifyId = get_data.get('tid')
            db_task = TbTask.query.filter(TbTask.id == specifyId)
            for i in db_task:
                is_img = i.is_orimg
                # 如果该条任务存在
                # 判断该任务的is_orimg字段值是否为1
                # 如果该字段不为1,则修改为1,即指定为模板
                if is_img != 1:
                    # 先把以前的is_orimg字段值为1的改为0,然后在修改新的ID的is_orimg字段值为1
                    try:
                        db.session.query(TbTask).filter(TbTask.is_orimg == "1").update({"is_orimg": "0"})
                        db.session.commit()
                    except Exception as e:
                        logger.error(f"更新原图状态:{traceback.format_exc()}行数:{e.__traceback__.tb_lineno}")
                        db.session.rollback()
                    # 修改字段值"is_orimg"为 1,即为任务模板
                    try:
                        db.session.query(TbTask).filter(TbTask.id == specifyId).update({"is_orimg": "1"})
                        db.session.commit()
                    except Exception as e:
                        logger.error(f"修改原图状态:{traceback.format_exc()}行数:{e.__traceback__.tb_lineno}")
                        db.session.rollback()
                    logger.info("指定任务为模板成功!")
                # 如果为1,则不作处理
                else:
                    pass
            return jsonify({'statusCode': 200, 'msg': '指定模板成功!'})
        except Exception as e:
            logger.error(f"指定原图模板异常:{traceback.format_exc()}行数:{e.__traceback__.tb_lineno}")
            return jsonify({'statusCode': 500, 'msg': 'fail'})

    # 任务图对比
    def contrast_analysis(self):
        try:
            get_data = request.get_json()
            route_id = get_data.get("rid")
            task_id = get_data.get("tid")
            route_id = int(route_id)
            task_id = int(task_id)
            result = TbTask.query.filter(TbTask.route_id == route_id)
            if result:
                for res in result:
                    # 如果数据中心的字段值is_orimg有1时，即有模板
                    if res.is_orimg == "1":
                        result1 = TbTask.query.filter(TbTask.id == task_id)
                        for res2 in result1:
                            path1 = os.path.join("D:/images/write_imgs/", res.task_name)
                            path2 = os.path.join("D:/images/write_imgs/", res2.task_name)
                            out_path = "D:/images/out_imgs/" + datetime.datetime.now().strftime("%Y%m%d%H%M%S") + "/"
                            if not os.path.exists(out_path):
                                os.makedirs(out_path, 755)
                            logger.info("out_path2: {}".format(out_path))
                            logger.info("开始修改对比状态")
                            try:
                                db.session.query(TbTask).filter(TbTask.id == task_id).update({"is_analysis": "2"})
                                db.session.commit()
                            except Exception as e:
                                logger.error(f"修改对比状态:{traceback.format_exc()}行数:{e.__traceback__.tb_lineno}")
                                db.session.rollback()
                            logger.info("对比状态修改成功")
                            # 开始对比
                            logger.info("开始对比")
                            Thread(target=contrast_floder, args=(path1, path2, out_path)).start()
                            logger.info("对比成功")
                            # 判断任务是否为有异物的任务
                            try:
                                db.session.query(TbTask).filter(TbTask.id == task_id).update({"tag": "1"})
                                db.session.commit()
                            except Exception as e:
                                logger.error(f"修改异物状态:{traceback.format_exc()}行数:{e.__traceback__.tb_lineno}")
                                db.session.rollback()
                            logger.info("异物状态修改成功")
                            # 修改图片对比状态
                            try:
                                db.session.query(TbImg).filter(TbImg.task_id == task_id).update({"is_analysis": "1"})
                                db.session.commit()
                            except Exception as e:
                                logger.error(f"提交失败:{traceback.format_exc()}行数:{e.__traceback__.tb_lineno}")
                                db.session.rollback()
                            logger.info("图片对比状态修改成功")
                            # 获取对比结果
                            result2 = TbAnalysis.query.filter(TbAnalysis.task_id == task_id)
                            res_list = []
                            for res3 in result2:
                                if res3.tag == "1":
                                    res_dic = {
                                        "id": res3.id,
                                        "tag": res3.tag,
                                        "score": res3.score,
                                        "box": res3.box,
                                        "img_name": res3.img_name,
                                        "img_url": res3.img_url,
                                        "task_id": res3.task_id,
                                        "create_time": str(res3.create_time),
                                    }
                                    res_list.append(res_dic)
                            return jsonify({"code": 200, "msg": "success", "result": res_list})
                    else:
                        # 指定原图
                        return jsonify({'code': 404, 'msg': 'error', 'data': '请先指定模板！'})
            else:
                return jsonify({"code": 501, "msg": "未在同一航线下,请重新选择"})
            logger.info("文件夹对比成功")

        except Exception as e:
            logger.error(f"文件夹图片分析异常:{traceback.format_exc()}行数:{e.__traceback__.tb_lineno}")
            return jsonify({'code': 404, 'msg': 'error', 'data': '文件夹对比异常！'})

    def contrast_data(self):
        # 交给线程去处理耗时任务
        # executor.submit(self.contrast_analysis())
        self.contrast_analysis()
        return jsonify({"statusCode": 200, "msg": "success"})

    @staticmethod
    def start():
        app.run(host='0.0.0.0', port=5008, debug=False)

server = API()
logger.info('[+] AGX API is running [%s]' % datetime.datetime.now())

if __name__ == '__main__':
    server.start()
