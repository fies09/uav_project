import base64
import json
from msg import json_response
from msg.messag import cs_image, sc_image
import detect
from tools import readImageTools
from tools import timeTools






#处理接收到的两张对比图片
def receive_image_data(jsondata):
    timeTools.printCurTime("收到消息")
    if len(jsondata) == 0:
        return json_response.JsonResponse.error()
    timeTools.printCurTime("开始解析json参数")
    receimagemsg = json.dumps(jsondata)
    receimagemsg = json.loads(receimagemsg)
    timeTools.printCurTime("解析完成")
    timeTools.printCurTime("开始执行图爿分析")
    tag,score,box,imgOut = detect.mainfundo(receimagemsg["current_base64"],receimagemsg["origin_base64"])
    timeTools.printCurTime("图片分析结束")
    scdata = dict()
    scdata["tag"] = tag
    scdata["box"] = box
    scdata["imgOut"] = readImageTools.img_to_base64(imgOut)
    timeTools.printCurTime("返回参数包装完成")

    sc_json_str = json.dumps(scdata)
    timeTools.printCurTime("返回参数json化完成，开始返回参数")
    return json_response.JsonResponse.success(sc_json_str).to_dict()





#处理接收到的两张对比图片
def receive_image(origin_image,current_image):
    timeTools.printCurTime("收到消息")

    timeTools.printCurTime("开始转图片转base64")
    current_base64 = base64.b64encode(current_image.read())
    origin_base64 = base64.b64encode(origin_image.read())
    timeTools.printCurTime("图片转base64 完成")

    timeTools.printCurTime("开始执行图爿分析")
    tag,score,box,imgOut = detect.mainfundo(current_base64,origin_base64)
    timeTools.printCurTime("图片分析结束")
    scdata = dict()
    scdata["tag"] = tag
    scdata["box"] = box
    scdata["imgOut"] = readImageTools.img_to_base64(imgOut)
    timeTools.printCurTime("返回参数包装完成")

    sc_json_str = json.dumps(scdata)
    timeTools.printCurTime("返回参数json化完成，开始返回参数")
    return json_response.JsonResponse.success(sc_json_str).to_dict()

