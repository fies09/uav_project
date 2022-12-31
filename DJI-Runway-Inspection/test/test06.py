import datetime
import threading
import time

# from queue import Queue
#
# q = Queue(maxsize=0)


# def product(name):
#     count = 1
#     while True:
#         q.put('气球兵{}'.format(count))
#         print('{}训练气球兵{}只'.format(name, count))
#         count += 1
#         time.sleep(5)
#
#
# def consume(name):
#     while True:
#         print('{}使用了{}'.format(name, q.get()))
#         time.sleep(1)
#         q.task_done()
#
#
# t1 = threading.Thread(target=product, args=('wpp',))
# t2 = threading.Thread(target=consume, args=('ypp',))
# t3 = threading.Thread(target=consume, args=('others',))
#
# t1.start()
# t2.start()
# t3.start()
from schema.models import TbTask, db

task_data = TbTask(task_name="DJI_202209051601_014_新建航点飞行4", route_name="新建航点飞行4", is_analysis='0',
                   is_orimg='0', route_id=2,
                   create_time=datetime.datetime.now())
db.session.add(task_data)
db.session.commit()
