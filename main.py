import os
import threading

import cv2

from decorators import timer, counter
from identify import Identify, categorize, show
from other_tasks import delete_expired_images, get_token
from config import Cimage, Oimage


# 初始化，建文件夹
def init():
    if not os.path.exists(Oimage):
        os.makedirs(Oimage)
    if not os.path.exists(Cimage):
        os.makedirs(Cimage)
    print('开始运行，正在准备模型...')


# 全局变量
frame = None


# 识别主体位置，截图，并用通用物体识别识别截过的图
def identify_main_object(filepath: str):
    ident = Identify(filepath)()
    return ident


# 定时截图并识别
@timer
@counter
def seeImage(count):
    global frame
    if frame is not None:
        filepath = os.path.join(Oimage, count + ".png")  # 保存路径
        cv2.imwrite(filepath, frame)
        ident = identify_main_object(filepath)
        show(*categorize(ident))


# 显示画面
def display_frame():
    global frame
    cap = cv2.VideoCapture(0)
    print('正在打开摄像头...')
    while True:
        # 从摄像头中读取画面，第一个参数ret的值为True或False，代表有没有读到图片。第二个参数frame，是当前截取一帧的图片
        _, frame = cap.read()
        # 显示窗口
        cv2.imshow('window', frame)
        # 按q退出
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
        # 点击窗口关闭按钮退出程序
        if cv2.getWindowProperty('window', cv2.WND_PROP_AUTOSIZE) < 1:
            break

    # 释放资源
    cap.release()
    # 关闭窗口
    cv2.destroyAllWindows()


if __name__ == '__main__':
    init()
    days = 3
    t1 = threading.Thread(target=delete_expired_images, args=(Cimage, days), daemon=True)  # 定期删除days天前的照片
    t2 = threading.Thread(target=get_token, daemon=True)  # 定期获取token
    t3 = threading.Thread(target=seeImage, daemon=True)  # 截图并识别

    t1.start()
    t2.start()
    t3.start()

    display_frame()
