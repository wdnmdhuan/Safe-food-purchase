import datetime
import time
from functools import wraps

from config import start, sleep


# 计时器：使函数每'sleep'时间运行一次
def timer(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        sched = start[func.__name__]
        while True:
            now = datetime.datetime.now()
            now = now - datetime.timedelta(microseconds=now.microsecond)
            if sched <= now:
                sched = now + datetime.timedelta(**sleep[func.__name__])
                func(*args, **kwargs)

    return wrapper


# 向函数传入日期和调用次数
def counter(func):
    num = [0]  # 闭包中外函数中的变量指向的引用不可变
    today = [""]

    @wraps(func)
    def wrapper(*args, **kwargs):
        if today[0] != time.strftime("%Y%m%d", time.localtime()):
            today[0] = time.strftime("%Y%m%d", time.localtime())
            num[0] = 0
        num[0] += 1
        return func(today[0] + "%05d" % num[0], *args, **kwargs)

    return wrapper
