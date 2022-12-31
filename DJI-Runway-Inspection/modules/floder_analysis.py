from datetime import datetime
import sys  # 导入模块
from modules import detect
from configs.log import logger
from schema.models import db, TbAnalysis, TbTask, TbImg
from tools import readImageTools
import cv2 as cv
import os


def add_prefix_files(path):  # 定义函数名称
    old_names = os.listdir(path)  # 取路径下的文件名，生成列表
    index = 1
    for old_name in old_names:  # 遍历列表下的文件名
        if old_name != sys.argv[0]:  # 代码本身文件路径，防止脚本文件放在path路径下时，被一起重命名
            if old_name.endswith('.JPG'):  # 当文件名以.txt后缀结尾时
                os.rename(os.path.join(path, old_name), os.path.join(path, str(index) + ".JPG"))  # 重命名文件
                logger.info(
                    "{0} has been renamed successfully! New name is: {1}".format(old_name, str(index) + ".JPG"))  # 输出提示
                index = index + 1

# 自动对比
def auto_compare(path1, file_path, fname, outpath):
    logger.info(">>>>>>>>>>>>>>>>开始执行自动对比功能>>>>>>>>>>>>>>>>")
    names1 = os.listdir(path1)
    for filename1 in names1:
        if filename1.split("_", 4)[-1] == fname.split("_", 4)[-1]:
            img1_base64 = readImageTools.image_to_base64(path1 + "/" + filename1)
            img2_base64 = readImageTools.image_to_base64(file_path + "/" + fname)
            task_name = file_path.split("/")[-1]
            results = TbTask.query.filter(TbTask.task_name == task_name)
            for task_data in results:
                imgout_name = outpath + filename1.replace(filename1.split("_", 4)[1], datetime.now().strftime("%Y%m%d%H%M%S"))
                tag, score, box, rectangle_img = detect.mainfundo(img2_base64, img1_base64)
                if tag:
                    filename = imgout_name.split("/", 4)[-1]
                    my_host = "http://124.89.8.210:3006"
                    url = my_host + imgout_name.split(":")[-1]
                    result2 = TbAnalysis.query.filter(TbAnalysis.img_name == filename).all()
                    if not result2:
                        logger.info("开始写入数据库")
                        result = TbAnalysis(tag=tag, score=str(score), box=str(box), img_name=filename, img_url=url,
                                            task_id=task_data.id, create_time=datetime.now())
                        db.session.add(result)
                        db.session.commit()
                        logger.info("数据库写入成功")
                    else:
                        logger.info("数据表已存在任务数据")
                    logger.info("开始保存异物框选图:{}".format(imgout_name.split('/')[-1]))
                    cv.imencode('.JPG', rectangle_img)[1].tofile(imgout_name)  # 将框住异物的图片保存
                    logger.info("异物框选图保存成功")
                else:
                    logger.info("对比图无异物")
                # 修改任务对对比状态
                logger.info("开始修改任务对比状态")
                db.session.query(TbTask).filter(TbTask.task_name == task_name).update({"is_analysis": "1"})
                db.session.commit()
                logger.info("任务对比状态修改成功")
            logger.info("开始修改任务进度")
            task_name = file_path.rsplit('/')[-1]
            num1 = len(os.listdir(file_path))
            num2 = len(os.listdir(outpath))
            task_process = str(num2) + "/" + str(num1)
            db.session.query(TbTask).filter(TbTask.task_name == task_name).update({"task_process": task_process})
            db.session.commit()
            logger.info("任务进度修改成功")
    logger.info(">>>>>>>>>>>>>>>自动对比功能执行成功>>>>>>>>>>>>>")


# 对比文件夹
def contrast_floder(path1, path2, outpath):
    logger.info(">>>>>>>>>>>>>>>>开始执行对比功能>>>>>>>>>>>>>>>>")
    names1 = os.listdir(path1)  # 取路径下的文件名，生成列表
    names2 = os.listdir(path2)  # 取路径下的文件名，生成列表
    for filename1 in names1:
        for filename2 in names2:
            if filename1.split("_", 4)[-1] == filename2.split("_", 4)[-1]:
                img1_base64 = readImageTools.image_to_base64(path1 + "/" + filename1)
                img2_base64 = readImageTools.image_to_base64(path2 + "/" + filename2)
                task_name = path2.split("/")[-1]
                results = TbTask.query.filter(TbTask.task_name == task_name)
                for task_data in results:
                    imgout_name = outpath + filename1.replace(filename1.split("_", 4)[1], datetime.now().strftime("%Y%m%d%H%M%S"))
                    tag, score, box, rectangle_img = detect.mainfundo(img2_base64, img1_base64)
                    if tag:
                        filename = imgout_name.split("/", 4)[-1]
                        my_host = "http://124.89.8.210:3006"
                        url = my_host + imgout_name.split(":")[-1]
                        result2 = TbAnalysis.query.filter(TbAnalysis.img_name == filename).all()
                        if not result2:
                            logger.info("开始写入数据库")
                            result = TbAnalysis(tag=tag, score=str(score), box=str(box), img_name=filename, img_url=url,
                                                task_id=task_data.id, create_time=datetime.now())
                            db.session.add(result)
                            db.session.commit()
                            logger.info("数据库写入成功")
                        else:
                            logger.info("数据表已存在任务数据")
                        cv.imencode('.JPG', rectangle_img)[1].tofile(imgout_name)  # 将框住异物的图片保存
                        logger.info("异物框选图保存成功")
                    else:
                        logger.info("对比图无异物")
                    # 修改任务对对比状态
                    logger.info("开始修改任务对比状态")
                    db.session.query(TbTask).filter(TbTask.task_name == task_name).update({"is_analysis": "1"})
                    db.session.commit()
                    logger.info("任务对比状态修改成功")
                logger.info("开始修改任务进度")
                task_name = path2.rsplit('/')[-1]
                num1 = len(os.listdir(path2))
                num2 = len(os.listdir(outpath))
                task_process = str(num2) + "/" + str(num1)
                db.session.query(TbTask).filter(TbTask.task_name == task_name).update({"task_process": task_process})
                db.session.commit()
                logger.info("任务进度修改成功")
    logger.info(">>>>>>>>>>>>>>>对比功能执行成功>>>>>>>>>>>>>")

if __name__ == '__main__':
    out_path = "D:/images/out_imgs/aaa"
    contrast_floder(r'D:/images/write_imgs/DJI_202209051601_011_新建航点飞行3',
                    r'D:/images/write_imgs/DJI_202209051601_013_新建航点飞行3', out_path)
