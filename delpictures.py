# -*- encoding: utf-8 -*-
# @Time      : 2020/12/12 20:19
# @Author    : zzh
# @File      : delpictures.py
from config import Cimage, Oimage
import os


# 删除Cimage, Oimage下的所有文件
def delete_pictures():
    for file in [os.path.join(Cimage, c) for c in os.listdir(Cimage)] \
                + [os.path.join(Oimage, o) for o in os.listdir(Oimage)]:
        os.remove(file)


if __name__ == '__main__':
    delete_pictures()
    print("完成")
