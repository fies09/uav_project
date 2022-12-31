#!/usr/bin/env python
# -*- coding = utf-8 -*-
# @Time       : 2022/9/7 14:20
# @Author     : fany
# @Project    : PyCharm
# @File       : main.py
# @description:
import datetime
import os
import shutil
import time
from threading import Thread
from configs import time_data
from schema.models import TbTask, db, TbRoute, TbAnalysis, TbImg
from server.maincontroller import API


def TimeStampToTime(timestamp):
    timeStruct = time.localtime(timestamp)
    return time.strftime('%Y-%m-%d %H:%M:%S', timeStruct)


def del_locdata():
    path1 = "D:/images/write_imgs/"
    path2 = "D:/images/out_imgs/"
    img_list = os.listdir(path1)
    for floder_name in img_list:
        file1_path = path1 + floder_name
        ctime = os.path.getctime(file1_path)
        ctime = TimeStampToTime(ctime)
        ctime = datetime.datetime.strptime(ctime, "%Y-%m-%d %H:%M:%S")
        now_date = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        now_date1 = datetime.datetime.strptime(now_date, "%Y-%m-%d %H:%M:%S")
        days = (now_date1 - ctime).days
        if days >= time_data['days']:
            shutil.rmtree(file1_path)

    img_list2 = os.listdir(path2)
    for floder_name2 in img_list2:
        file2_path = path2 + floder_name2
        ctime = os.path.getctime(file2_path)
        ctime = TimeStampToTime(ctime)
        ctime = datetime.datetime.strptime(ctime, "%Y-%m-%d %H:%M:%S")
        now_date = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        now_date1 = datetime.datetime.strptime(now_date, "%Y-%m-%d %H:%M:%S")
        days = (now_date1 - ctime).days
        if days >= time_data['days']:
            shutil.rmtree(file2_path)


def del_sqldata():
    # 对分析表数据进行处理
    s4 = TbAnalysis.query.all()
    for res4 in s4:
        t_time = res4.create_time
        now_date = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        now_date1 = datetime.datetime.strptime(now_date, "%Y-%m-%d %H:%M:%S")
        duration = now_date1 - t_time
        days = duration.days
        db.session.query(TbTask).filter(days >= time_data['days']).delete()
        db.session.commit()

    # 对图片表数据进行处理
    s3 = TbImg.query.all()
    for res3 in s3:
        t_time = res3.create_time
        now_date = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        now_date1 = datetime.datetime.strptime(now_date, "%Y-%m-%d %H:%M:%S")
        duration = now_date1 - t_time
        days = duration.days
        db.session.query(TbTask).filter(days >= time_data['days']).delete()
        db.session.commit()

    # 对任务表数据进行处理
    s1 = TbTask.query.all()
    for res1 in s1:
        t_time = res1.create_time
        now_date = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        now_date1 = datetime.datetime.strptime(now_date, "%Y-%m-%d %H:%M:%S")
        days = (now_date1 - t_time).days
        db.session.query(TbTask).filter(days >= time_data['days']).delete()
        db.session.commit()

    # 对航线表数据进行处理
    s2 = TbRoute.query.all()
    for res2 in s2:
        t_time = res2.create_time
        now_date = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        now_date1 = datetime.datetime.strptime(now_date, "%Y-%m-%d %H:%M:%S")
        duration = now_date1 - t_time
        days = duration.days
        db.session.query(TbTask).filter(days >= time_data['days']).delete()
        db.session.commit()


def task_main():
    # Thread(target=download_file).start()
    Thread(target=del_locdata).start()
    Thread(target=del_sqldata).start()
    API.start()

if __name__ == '__main__':
    task_main()
