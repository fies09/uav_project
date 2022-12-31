import time
from concurrent.futures import ThreadPoolExecutor
from flask import Flask, signals, g
executor = ThreadPoolExecutor()


app = Flask(__name__)

# executor = ThreadPoolExecutor(10)里面的数字是线程池所能同时进行的最大数量
['DJI_20220905161104_0001_Z_航点1.JPG',
 'DJI_20220905161117_0002_Z_航点2.JPG',
 'DJI_20220905161132_0003_Z_航点3.JPG',
 'DJI_20220905161146_0004_Z_航点4.JPG',
 'DJI_20220905161206_0005_Z_航点5.JPG',
 'DJI_20220905161358_0001_Z_航点1.JPG',
 'DJI_20220905161411_0002_Z_航点2.JPG',
 'DJI_20220905161426_0003_Z_航点3.JPG', 'DJI_20220905161439_0004_Z_航点4.JPG', 'DJI_20220905161500_0005_Z_航点5.JPG', 'DJI_20220905161634_0001_Z_航点1.JPG', 'DJI_20220905161646_0002_Z_航点2.JPG', 'DJI_20220905161701_0003_Z_航点3.JPG', 'DJI_20220905161715_0004_Z_航点4.JPG', 'DJI_20220905161735_0005_Z_航点5.JPG', 'DJI_20220908111145_0001_Z.JPG', 'DJI_20220908111247_0002_Z.JPG', 'DJI_20220908111420_0003_Z.JPG', 'DJI_20220908111634_0001_Z.JPG', 'DJI_20220908111744_0002_Z.JPG', 'DJI_20220908112553_0003_Z.JPG', 'DJI_20220908120107_0001_Z.JPG', 'DJI_20220908120213_0002_Z.JPG', 'DJI_20220908120216_0003_Z.JPG', 'DJI_20220908120247_0004_Z.JPG', 'e3dea0f5-37f2-4d79-ae58-490af3228069', 'org_13edf1bc163b925c_1662607064000.jpg', 'org_228cd71222fdece3_1662607552000.jpg', 'org_283838a199329ddf_1662617458000.jpg', 'org_c2d499b3bf8f4b88_1662609666000.jpg', 'org_e0d91003baa85946_1662365196000.jpg', 'org_e8426c6433f485e3_1662366180000.jpg']
def run():
    time.sleep(10)
    print("耗时任务执行结束")


@app.route('/test')
def test():
    # 交给线程去处理耗时任务
    executor.submit(run)
    return "cheer!"


if __name__ == '__main__':
    app.run()