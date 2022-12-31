项目说明

####1. 目录结构描述 
├──  configs               // 配置文件目录
│    ├──  __init__.py        // 配置文件
│    ├──  log.py             // log的输出配置文件
├──  DOC               // 文档目录
│    ├──  README.md    // 项目说明
│    ├──  requirements.txt   // 环境配置文件
├──  images                  // 文件存储目录
├──  logs                  // 日志存放目录
├──  modules                // 每一个文件为一个功能模块,供API调用
│    ├──  mainManage.py          // 图片解析主程序
│    ├──  changefilename.py     // 文件夹对比
│    ├──  detect.py       // 检查异物
│    ├──  rectangle.py     // 标注异物
├──  msg                 
│    ├──  json_response.py   //返回值格式声明
│    ├──  message.py        // 接收对比的参数
├──  test                 // 常用配置工具目录
├──  tools                // API接口主程序
│    ├──  readImageTools.py    // 格式转换
│    ├──  timeTools.py    // 时间+字符串输出
│    ├──  tool.py       // 定义的验证登录状态的装饰器
├──  maincontroller.py    // 程序主入口
####2. api返回值：
返回值定义格式：
# 返回成功
msg = Msg()
return msg.meta({'key': 'val'}).success(msg='str', result=results).json()

# 返回失败
msg = Msg()
return msg.fail(msg='str失败').json()

返回值返回格式：
# 接收成功
{'code': 0, 'status': True, 'msg': 'str', 'data': {'meta': {'key': 'val'}, 'result': {}}}

# 接收失败
{'code': 1, 'status': False, 'msg': 'str失败', 'data': {}}

- 说明： 
- code：0表示正常 1表示异常 
- status：True表示正常 False表示异常
- msg：说明信息，str类型填写
- data: 返回数据，目前容量为两个，mete一般返回数量，result返回数据结果。

日志输出格式:
logger.info("{}".format())

安装第三方模块:
    pip3 install pipreqs
生成配置文件requirements.txt,在项目根目录下执行
    pipreqs ./ --encoding=utf8 --force
参数说明:当要更新配置文件时,"--force"会覆盖之前生成的配置文件

# 启动服务命令
pm2 start C:/Users/Administrator/Desktop/DJI-Runway-In
spection/DJI-Runway-Inspection/main.py -x -interpreter python