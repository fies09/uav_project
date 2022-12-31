#!/usr/bin/env python
# -*- coding = utf-8 -*-
# @Time       : 2022/8/25 11:33
# @Author     : fany
# @Project    : PyCharm
# @File       : file_path.py
# @description:
import os
from os import path
from configs.log import logger
# 获取当前位置的绝对路径
basedir = os.path.abspath(os.path.dirname(__file__))

filepath = path.dirname(basedir)
logger.info(filepath)