#!/usr/bin/env python
# -*- coding = utf-8 -*-
# @Time       : 2022/8/25 14:45
# @Author     : fany
# @Project    : PyCharm
# @File       : query.py
# @description:
import datetime
import os
import time

from schema.models import TbTask, db, TbRoute, TbAnalysis

filoder_path = "D:/images/write_imgs"
floder_name = os.listdir(filoder_path)
floder_name.sort(key=lambda fn: os.path.getmtime(filoder_path + "/" + fn))
task_name = floder_name[-5]
route_name = task_name.split("_")[-1]
img_name = os.listdir(filoder_path + "/" + task_name)
my_host = "http:/124.89.8.210:3006"
imgUrl_list = []
for file_name in img_name:
    img_url = my_host + "/" + filoder_path.split("/", 1)[-1] + file_name
    imgUrl_list.append(img_url)
# 向任务表插入数据
# task_data = TbTask(task_name=task_name, route_name=route_name, image_names=str(img_name), image_urls=str(imgUrl_list),
#                    create_time=datetime.datetime.now())
# db.session.add(task_data)
# db.session.commit()

# 向航线表插入数据
task_data = TbTask.query.filter(TbTask.route_name==route_name).first()
task_id = task_data.id
route_data = TbRoute(route_name=route_name, create_time=datetime.datetime.now(), task_id=task_id)
db.session.add(route_data)
db.session.commit()
