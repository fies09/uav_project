import os,sys                       #导入模块
import detect
from tools import readImageTools
import cv2 as cv


def add_prefix_files(path):             #定义函数名称
    old_names = os.listdir( path )  #取路径下的文件名，生成列表
    index = 1
    for old_name in old_names:      #遍历列表下的文件名
            if  old_name!= sys.argv[0]:  #代码本身文件路径，防止脚本文件放在path路径下时，被一起重命名
               if old_name.endswith('.JPG'):   #当文件名以.txt后缀结尾时
                    os.rename(os.path.join(path,old_name),os.path.join(path,str(index)+".JPG"))  #重命名文件
                    print (old_name,"has been renamed successfully! New name is: ",str(index)+".JPG")  #输出提示
                    index = index + 1


#对比文件夹
def contrast_floder(path1,path2,outpath):
    names1 = os.listdir(path1)  # 取路径下的文件名，生成列表
    names2 = os.listdir(path2)  # 取路径下的文件名，生成列表
    if len(names1) != len(names2):
        print("两组图片对比失败，因为文件数量不统一")
        return
    index = 1
    for cur in names1:
        print("开始执行当前文件："+str(index))
        img1_base64 = readImageTools.image_to_base64(path1+"/"+str(index)+".JPG")
        img2_base64 = readImageTools.image_to_base64(path2 + "/" + str(index) + ".JPG")
        imgout_name =  outpath+ "/" + str(index) + ".JPG"
        tag,score,box,rectangle_img = detect.mainfundo(img2_base64,img1_base64)
        if tag:
            print("异常:" + path2 + "/" + str(index) + ".JPG")
            cv.imwrite(imgout_name, rectangle_img) # 将框住异物的图片保存
        else:
            print("正常:"+path2 + "/" + str(index) + ".JPG")

        index = index + 1

    print("done.")




if __name__ == '__main__':
    # add_prefix_files(r'./images/image2')         #调用定义的函数，注意名称与定义的函数名一致
    contrast_floder(r'./images/image1', r'./images/image2', r'./images/yiwu1-2')



