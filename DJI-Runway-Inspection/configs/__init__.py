#!/usr/bin/env python
# -*- coding = utf-8 -*-
# @Time       : 2022/8/23 16:04
# @Author     : fany
# @Project    : PyCharm
# @File       : __init__.py
# @description:
from celery import Celery
DEBUG = True

img_information = {
    'img_path': "./images/",  # 图片文件夹路径
    'img_current_name': '9-2.jpg',  # img_current文件名
    'img_origin_name': '9-1.jpg',  # img_origin文件名
    'size': 12,  # 开运算操作核大小:默认为12
    'threshold': 60  # 分割的阈值:默认为60
    }

db_mysql = {
    'host': '127.0.0.1',
    'port': '3306',
    'database': "db_runway",
    'user': "root",
    'pwd': "Ytwl@2022!",
}

oss_config = {
    "endpoint": "https://oss-cn-beijing.aliyuncs.com",
    "accesskey_id": "LTAI5tCMxPJeZfwsAoTxRgBb",
    "accesskey_secret": "yC6cXxd0ad8n4Ec042Gzu6j1L0fyg0",
    "bucket_name": "ytwl-jichang",
}

time_data = {
    "days": 90
}

