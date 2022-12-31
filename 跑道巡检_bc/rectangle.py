import cv2
from concurrent.futures import ProcessPoolExecutor


def foreign_body(img, x, y, x_step, y_step):
    tag = False  # 标志位：是否有异物
    bottom, right = 0, 0  # 右下
    top, left = float('inf'), float('inf')  # 左上
    x_final = x + x_step
    y_final = y + y_step
    for i in range(x, x_final,2):
        for j in range(y, y_final,2):
            if img[i][j] != 0:
                tag = True
                # print(f'{x=},{y=}:{img[x][y]=}')
                top = min(i, top)
                bottom = max(i, bottom)
                left = min(j, left)
                right = max(j, right)

    # print(f'{tag}:{top=},{bottom=},{left=},{right=}')
    if tag:
        return tag, [top, bottom, left, right]
    else:
        return False, []


def compute_startpoint(shape):
    # 计算起始点坐标
    x_step = shape[0] // 3
    y_step = shape[1] // 3
    start_point = []
    x, y = 0, 0
    for i in range(1, 10):
        start_point.append([x, y])
        y += y_step
        if i % 3 == 0:
            x += x_step
            y = 0
    return start_point


def draw_rectangle(img, imgOut):
    start_point = compute_startpoint(img.shape)
    x_step = img.shape[0] // 3
    y_step = img.shape[1] // 3
    rectangle_pos = []
    pool = ProcessPoolExecutor(max_workers=16)

    tasks = [pool.submit(foreign_body, img, x, y, x_step, y_step) for x, y in start_point]
    for t in tasks:
        tag = t.result()[0]
        pos = t.result()[1]
        if tag:
            cv2.rectangle(imgOut, (pos[2]-20, pos[0]-20), (pos[3]+20, pos[1]+20), (0, 0, 255), 2)
            rectangle_pos.append(pos)

    if len(rectangle_pos) != 0:
        return True, rectangle_pos, imgOut
    else:
        return False, [], []
