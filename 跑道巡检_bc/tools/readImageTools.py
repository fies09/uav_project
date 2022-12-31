# 文件流形式读取为图片数据
import base64
import skimage.io
import cv2
import base64
import numpy as np


# 图片转base64
def img_to_base64(img_array):
    # 传⼊图⽚为RGB格式numpy矩阵，传出的base64也是通过RGB的编码
    img_array = cv2.cvtColor(img_array, cv2.COLOR_RGB2BGR)#RGB2BGR，⽤于cv2编码
    encode_image = cv2.imencode(".jpg", img_array)[1]#⽤cv2压缩/编码，转为⼀维数组
    byte_data = encode_image.tobytes()#转换为⼆进制
    base64_str = base64.b64encode(byte_data).decode("ascii")#转换为base64
    return base64_str


#base64转图片
def base64_to_img(base64_str):
    # 传⼊为RGB格式下的base64，传出为RGB格式的numpy矩阵
    byte_data = base64.b64decode(base64_str)#将base64转换为⼆进制
    encode_image = np.asarray(bytearray(byte_data), dtype="uint8")# ⼆进制转换为⼀维数组
    img_array = cv2.imdecode(encode_image, cv2.IMREAD_COLOR)# ⽤cv2解码为三通道矩阵
    img_array = cv2.cvtColor(img_array, cv2.COLOR_BGR2RGB)# BGR2RGB
    return img_array



#base64转rgb数组
def base64_to_rgb(base64_str):
    if isinstance(base64_str,bytes):
        base64_str = base64_str.decode("utf-8")

    imgdata = base64.b64decode(base64_str)
    img = skimage.io.imread(imgdata,plugin="imageio")
    return img


#图爿转base64
def cv2_base64(image):
    base64_str = cv2.imencode('.jpg',image)[1].tobytes()
    base64_str = base64.b64encode(base64_str)
    return base64_str.decode("utf-8")

#文件名转成base64
def image_to_base64(image_filepath):
    try:
      img = cv2.imread(image_filepath)
      print(img.shape)
      img_64 = cv2_base64(img)
    except Exception as e:
      print(e)
    return img_64
