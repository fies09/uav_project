#!/usr/bin/env python
# -*- coding = utf-8 -*-
# @Time       : 2022/9/7 14:13
# @Author     : fany
# @Project    : PyCharm
# @File       : sql_insert.py
# @description:
import datetime
import os
import traceback

from configs.log import logger
from schema.models import TbTask, db, TbRoute, TbImg

path = "D:/images/write_imgs/"


# 向航线表插入数据
def insert_route(floder_name):
    route_name = floder_name.rsplit("_")[-1]
    result = TbRoute.query.filter(TbRoute.route_name == route_name).all()
    if not result:
        logger.info("开始向航线表插入数据")
        route_data = TbRoute(route_name=route_name, create_time=datetime.datetime.now())
        try:
            db.session.add(route_data)
            db.session.commit()
        except Exception as e:
            logger.error(f"向航线表插入数据异常:{traceback.format_exc()}行数:{e.__traceback__.tb_lineno}")
            db.session.rollback()
        logger.info("航线表数据插入成功")
    else:
        logger.info("航线数据已存在")


# 向任务表插入数据
def insert_task(floder_name):
    route_name = floder_name.rsplit("_")[-1]
    results = TbTask.query.filter(TbTask.task_name == floder_name).all()
    if not results:
        result = TbRoute.query.filter(TbRoute.route_name == route_name)
        for data in result:
            num = len(os.listdir(path + '/' + floder_name))
            task_process = str(0) + "/" + str(num)
            logger.info("开始向任务数据表插入数据")
            task_data = TbTask(task_name=floder_name, route_name=route_name, task_process=task_process,
                               route_id=data.id, create_time=datetime.datetime.now())
            try:
                db.session.add(task_data)
                db.session.commit()
            except Exception as e:
                logger.error(f"向任务表插入数据异常:{traceback.format_exc()}行数:{e.__traceback__.tb_lineno}")
                db.session.rollback()
            logger.info("任务数据插入成功")
    else:
        logger.info("任务数据已存在")


# 向图片表写入数据
def insert_img(fname, floder_name):
    my_host = "http://124.89.8.210:3006"
    path1 = path + floder_name
    image_url = my_host + path1.split(':')[-1] + '/' + fname
    result = TbTask.query.filter(TbTask.task_name == floder_name)
    result2 = TbImg.query.filter(TbImg.img_name == fname).all()
    for res1 in result:
        task_id = res1.id
        if not result2:
            # 执行插入操作
            logger.info("开始向图片表插入数据")
            db_img = TbImg(img_name=fname, img_url=image_url, task_id=task_id,
                           create_time=datetime.datetime.now())
            try:
                db.session.add(db_img)
                db.session.commit()
            except Exception as e:
                logger.error(f"向图片表插入数据异常:{traceback.format_exc()}行数:{e.__traceback__.tb_lineno}")
                db.session.rollback()
            logger.info("图片数据插入成功")
        else:
            logger.info("图片数据已存在")


# if __name__ == '__main__':
#     fname = "DJI_20220905161646_0002_Z_航点2.JPG"
#     floder_name = "DJI_202209051601_013_新建航点飞行3"
#     insert_img(fname, floder_name)
