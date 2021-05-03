import os
import json
import datetime
import requests
from decorators import timer


# 定时删除过期图片
@timer
def delete_expired_images(pathname: str, day_difference: int):
    """
    删除day_difference天前的pathname路径下的图片

    :param pathname: 要删除的文件夹的路径
    :param day_difference: 几天过期
    :return: None
    """
    if not os.path.exists(pathname):
        raise Exception("Path doesn't exist.")
    for filename in os.listdir(pathname):
        filepath = os.path.join(pathname, filename)
        date = datetime.datetime.fromtimestamp(os.path.getmtime(filepath))
        now = datetime.datetime.now()
        if (now - date).days > day_difference:
            if os.path.exists(filepath):
                os.remove(filepath)
                print('remove file: %s' % filepath)
            else:
                print('no such file: %s' % filepath)


# 定时获取新的token
@timer
def get_token():
    with open("data/token.json") as f:
        applications = json.load(f)

    for key, application in applications.items():
        host = f'https://aip.baidubce.com/oauth/2.0/token?' \
               f'grant_type=client_credentials&' \
               f'client_id={application["AK"]}&' \
               f'client_secret={application["SK"]}'
        response = requests.get(host)
        if response:
            application["token"] = response.json()["access_token"]
            applications[key] = application
    with open("data/token.json", 'w') as f:
        json.dump(applications, f)
