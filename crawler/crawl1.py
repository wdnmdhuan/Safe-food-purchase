# -*- encoding: utf-8 -*-
# @Time      : 2021/4/21 19:43
# @Author    : zzh
# @File      : crawl1.py

import time
import random
import requests


def id2ft(food_id, poj):
    base_url = 'https://spcjsac.gsxt.gov.cn/api/goods/info'
    headers = {
        'Host': 'spcjsac.gsxt.gov.cn',
        'Origin': 'https://spcjsac.gsxt.gov.cn',
        'Referer': 'https://spcjsac.gsxt.gov.cn/detail.html?type_id=&foodId=446033&goods_enterprise=/',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
                      'AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/90.0.4430.85 Safari/537.36',
    }
    # for i in range(200):
    data = {
        # 'food_type': 'a',
        'food_id': f'{food_id}',
        'goods_enterprise': poj,
        # 'pageNumber': '1',
        # 'pageSize': '10',
    }
    response = requests.post(base_url, data=data, headers=headers)
    return response.json()


def foods_info():
    base_url = 'https://spcjsac.gsxt.gov.cn/api/goods/data'
    headers = {
        'Host': 'spcjsac.gsxt.gov.cn',
        'Origin': 'https://spcjsac.gsxt.gov.cn',
        'Referer': 'https://spcjsac.gsxt.gov.cn/',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
                      'AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/90.0.4430.85 Safari/537.36',
    }
    for i in range(1, 35000):
        data = {
            'pageNumber': f'{i}',
            # 'pageSize': '10',
            'check_flag': 'uq'
        }
        response = requests.post(base_url, data=data, headers=headers)
        # print(response.json())
        for j in response.json()['data']['rows']:
            yield j
        time.sleep(random.random() * 2)


# for food in foods_info():
#     print(food)  # 这里改成写入文件 csv格式
print(id2ft(4579181, '乐陵市清波蔬菜经营中心（邵清波）')['data']['rows'][0]['check_list'])
