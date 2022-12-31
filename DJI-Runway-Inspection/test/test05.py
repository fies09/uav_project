#!/usr/bin/env python
# -*- coding = utf-8 -*-
# @Time       : 2022/9/7 16:03
# @Author     : fany
# @Project    : PyCharm
# @File       : test05.py
# @description:
# from schema.models import TbTask
# results = TbTask.query.all()
# result_dic = {}
# result_list = []
# for result in results:
#     result_dic["id"] = result.id
#     result_dic['task_name'] = result.task_name
#     result_dic["create_time"] = result.create_time
#     result_list.append(result_dic)
#     print(result_list)

from schema.models import TbTask

result = TbTask.query.all()
for re_i in result:
    print(re_i.task_name)
