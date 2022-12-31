# conding = utf-8
from schema.models import TbTask
import json


def get_taskStatus():
    result = TbTask.query.filter(TbTask.is_orimg == 1)
    for res in result:
        print(res.is_analysis)
        # return json.dumps({"code": 200, "status": res.is_analysis})


if __name__ == '__main__':
    get_taskStatus()
