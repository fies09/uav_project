import datetime
import os

from schema.models import TbImg, db, TbTask
# path1 = "D:/images/write_imgs/DJI_202209051601_014_新建航点飞行4"
path2 = "D:/images/write_imgs/DJI_202209051601_015_新建航点飞行4"
# floder1_name = "DJI_202209051601_014_新建航点飞行4"
floder2_name = "DJI_202209051601_015_新建航点飞行4"
my_host = "http://124.89.8.210:3006"
# for file1_name in os.listdir(path1):
#     result = TbTask.query.filter(TbTask.task_name == floder1_name)
#     for i in result:
#         image_url = my_host + path1.split(':')[-1] + '/' + file1_name
#         # print(file1_name)
#         # print(image_url)
#         # print(i.id)
#
#         db_img = TbImg(img_name=file1_name, img_url=image_url, is_analysis='0', task_id=i.id, ceate_time=datetime.datetime.now())
#         db.session.add(db_img)
#         db.session.commit()

for file2_name in os.listdir(path2):
    result = TbTask.query.filter(TbTask.task_name == floder2_name)
    for i in result:
        image_url = my_host + path2.split(':')[-1] + '/' + file2_name
        db_img = TbImg(img_name=file2_name, img_url=image_url, is_analysis='0', task_id=i.id, ceate_time=datetime.datetime.now())
        db.session.add(db_img)
        db.session.commit()