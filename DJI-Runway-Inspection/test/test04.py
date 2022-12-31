#!/usr/bin/env python
# -*- coding = utf-8 -*-
# @Time       : 2022/9/6 17:50
# @Author     : fany
# @Project    : PyCharm
# @File       : test04.py
# @description:
from schema.models import TbTask
import os,datetime
from modules.floder_analysis import add_prefix_files, contrast_floder
list1 = TbTask.query.filter(TbTask.route_name == "机场灯光2由东至西").first()
lists = TbTask.query.filter(TbTask.route_name == "机场灯光2由东至西").all()
for list2 in lists:
    if list2.task_name != list1.task_name:
        out_path = "D:/images/out_imgs/" + datetime.datetime.now().strftime("%Y%m%d%H%M%S") + "/"
        if not os.path.exists(out_path):
            os.makedirs(out_path, 755)
        path1 = "D:/images/write_imgs/" + list1.task_name
        path2 = "D:/images/write_imgs/" + list2.task_name
        add_prefix_files(path1)
        add_prefix_files(path2)
        print("111")
        contrast_floder(path1, path2, out_path)
        print("222")

# out_path = "D:/images/out_imgs/" + datetime.datetime.now().strftime("%Y%m%d%H%M%S") + "/"
# if not os.path.exists(out_path):
#     os.makedirs(out_path, 755)
# for list2 in lists:
#     if list2 != list1:
#         contrast_floder(list1, list2, out_path)
#         res = TbAnalysis.query.filter(TbAnalysis.id == TbTask.tb_analysis_id).update(
#             TbAnalysis.is_analysis == "1")
#         db.session.add(res)
#         db.session.commit()
