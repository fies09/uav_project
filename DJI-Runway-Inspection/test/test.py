#!/usr/bin/env python
# -*- coding = utf-8 -*-
# @Time       : 2022/8/25 10:40
# @Author     : fany
# @Project    : PyCharm
# @File       : test.py
# @description:
import os
# 获取当前位置的绝对路径
# basedir = os.path.abspath(os.path.dirname(__file__))
# file_path = os.path.dirname(basedir) + "\\static\\file"
# if not os.path.exists(file_path):
#     os.makedirs(file_path, 755)

file_path1 = "D:/images/"
lists = os.listdir(file_path1)
lists.sort(key=lambda fn: os.path.getmtime(file_path1 + "\\" + fn))
print(lists)