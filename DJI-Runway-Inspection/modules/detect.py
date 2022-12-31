from skimage import io
import cv2 as cv
import numpy as np
from skimage.metrics import structural_similarity as ssim

from configs.log import logger
from modules import rectangle
import configs
from tools import readImageTools, timeTools


def registration_orb(img_current, img_origin):  # orb配准
    orb = cv.ORB_create(nfeatures=700, scaleFactor=2)
    img1, img2 = img_origin, img_current
    kp1, des1 = orb.detectAndCompute(img1, None)
    kp2, des2 = orb.detectAndCompute(img2, None)

    bf = cv.BFMatcher(cv.NORM_HAMMING, crossCheck=True)  # create BFMatcher object
    matches = bf.match(des1, des2)  # Match descriptors.
    matches = sorted(matches, key=lambda x: x.distance)  # Sort them in the order of their distance.

    goodMatch = matches[:20]
    if len(goodMatch) > 4:
        ptsA = np.float32([kp1[m.queryIdx].pt for m in goodMatch]).reshape(-1, 1, 2)
        ptsB = np.float32([kp2[m.trainIdx].pt for m in goodMatch]).reshape(-1, 1, 2)
        ransacReprojThreshold = 4
        H, status = cv.findHomography(ptsA, ptsB, cv.RANSAC, ransacReprojThreshold);
        imgOut = cv.warpPerspective(img2, H, (img1.shape[1], img1.shape[0]),
                                    flags=cv.INTER_LINEAR + cv.WARP_INVERSE_MAP)

        score = ssim(cv.cvtColor(img1, cv.COLOR_RGB2GRAY), cv.cvtColor(imgOut, cv.COLOR_RGB2GRAY))

        err = cv.absdiff(img1, imgOut)  # 差分图像
        h, w, c = err.shape
        err = err[int(h * 0.05):int(h * 0.95), int(w * 0.05):int(w * 0.95)]  # 裁切
        imgOut = imgOut[int(h * 0.05):int(h * 0.95), int(w * 0.05):int(w * 0.95)]
        return err, imgOut, score


def threshold_segmentation(img, threshold):  # 分割
    maxval = 255
    dst, threh_img = cv.threshold(img, threshold, maxval, cv.THRESH_BINARY)
    return threh_img


def erode_dilate(img, size):  # 开运算
    kernel = cv.getStructuringElement(cv.MORPH_RECT, (size, size))

    dst = cv.erode(img, kernel)  # 腐蚀
    res = cv.dilate(dst, kernel)  # 膨胀

    return res


def detection(img_current_path, img_origin_path, size, threshold):
    """
    检测异物
    :param img_current_path:当前图像路径
    :param img_origin_path:原始图像路径
    :param size:开运算操作核大小,默认为12
    :param threshold:分割的阈值,默认为60
    :return:
    如果标志位tag == Ture:
    返回True, score:相似度得分 box：异物坐标，rectangle_img标注异物的图片
        标志位tag == False:
    返回False
    """
    img_current = io.imread(img_current_path)
    img_origin = io.imread(img_origin_path)
    img_current = np.uint8(img_current)
    img_origin = np.uint8(img_origin)

    err, imgOut, score = registration_orb(img_current, img_origin)
    err = cv.cvtColor(err, cv.COLOR_RGB2GRAY)
    threh_img = threshold_segmentation(err, threshold)
    erode_dilate_img = erode_dilate(threh_img, size)
    tag, box, rectangle_img = rectangle.draw_rectangle(erode_dilate_img, imgOut)
    if tag:
        return True, score, box, rectangle_img
        # 返回score:相似度得分 box：异物坐标，rectangle_img标注异物的图片
    else:
        return False, None, None, None


# 检测方法add.blf by 20220802
# 通过base64方法
def detection_2(img_current_base64, img_origin_base64, size, threshold):
    """
    检测异物
    :param img_current_path:当前图像路径
    :param img_origin_path:原始图像路径
    :param size:开运算操作核大小,默认为12
    :param threshold:分割的阈值,默认为60
    :return:
    如果标志位tag == Ture:
    返回True, score:相似度得分 box：异物坐标，rectangle_img标注异物的图片
        标志位tag == False:
    返回False
    """
    # 文件读取rgb
    timeTools.printCurTime("图片分析 -- 开始执行base64->rgb数组")
    img_current = readImageTools.base64_to_rgb(img_current_base64)
    img_origin = readImageTools.base64_to_rgb(img_origin_base64)
    #
    timeTools.printCurTime("图片分析 -- 开始执行 uint8 ")
    img_current = np.uint8(img_current)
    img_origin = np.uint8(img_origin)

    timeTools.printCurTime("图片分析 --  开始执行差分运算 ")
    err, imgOut, score = registration_orb(img_current, img_origin)

    timeTools.printCurTime("图片分析 --  开始执行阈值分割 ")
    err = cv.cvtColor(err, cv.COLOR_RGB2GRAY)
    threh_img = threshold_segmentation(err, threshold)

    timeTools.printCurTime("图片分析 --  开始执行 开运算 ")
    erode_dilate_img = erode_dilate(threh_img, size)

    tag, box, rectangle_img = rectangle.draw_rectangle(erode_dilate_img, imgOut)
    if tag:
        logger.info("")
        return True, score, box, rectangle_img
        # 返回score:相似度得分 box：异物坐标，rectangle_img标注异物的图片
    else:
        return False, None, None, None


def mainfundo(image_current, image_origin):
    tag, score, box, rectangle_img = detection_2(image_current, image_origin,
                                                 size=configs.img_information['size'],
                                                 threshold=configs.img_information['threshold'])

    if tag:
        print(f'是否存在异物:{tag}\n'
              f'相似度得分为:{score}\n'
              f'异物坐标为：{box}')
        # cv.imwrite('rectangle_img4_yiwu5', rectangle_img) # 将框住异物的图片保存
        # cv.namedWindow('rectangle', 0)
        # cv.imshow('rectangle', rectangle_img)
        timeTools.printCurTime("结束时间")
        return tag, score, box, rectangle_img

    else:
        print(f'是否存在异物:{tag}')
        timeTools.printCurTime("结束时间")
        return tag, None, None, None


if __name__ == '__main__':
    timeTools.printCurTime("开始时间")
    img_current_path = configs.img_information['img_path'] + configs.img_information['img_current_name']
    img_origin_path = configs.img_information['img_path'] + configs.img_information['img_origin_name']
    tag, score, box, rectangle_img = detection(img_current_path, img_origin_path,
                                               size=configs.img_information['size'],
                                               threshold=configs.img_information['threshold'])

    if tag:
        print(f'是否存在异物:{tag}\n'
              f'相似度得分为:{score}\n'
              f'异物坐标为：{box}')
        # cv.imwrite('rectangle_img4_yiwu5', rectangle_img) # 将框住异物的图片保存
        cv.namedWindow('rectangle', 0)
        cv.imshow('rectangle', rectangle_img)
        timeTools.printCurTime("结束时间")
        cv.waitKey(0)

    else:
        print(f'是否存在异物:{tag}')
        timeTools.printCurTime("结束时间")
