# -*- encoding: utf-8 -*-
# @Time      : 2021/4/21 16:32
# @Author    : zzh
# @File      : crawl.py
import random
import time

import requests
from bs4 import BeautifulSoup

# 爬取新闻

headers = {
    'Cookie': '__yjs_duid=1_741b710bf66ffb39e0c47c58ee08efa21619674176461; '
              'PHPSESSID=k1pv85cb838vpgog73139gu645; '
              'stattraffic_sitekeyword=%E9%A3%9F%E5%93%81%2C%E9%A3%9F%E5%93%81%E5%AE%89%E5%85%A8%2C%E9%A3%9F%E5%93%81%E8%A1%8C%E4%B8%9A%2C%E9%A4%90%E9%A5%AE%2C%E9%A5%AE%E9%A3%9F%2C%E5%BF%AB%E9%A4%90%2C%E9%A5%AE%E6%96%99%2C%E5%86%9C%E4%BA%A7%E5%93%81',
    'Host': 'www.cfnews.com.cn',
    'Referer': 'http://www.cfnews.com.cn/toutiao.html',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
                  'AppleWebKit/537.36 (KHTML, like Gecko) '
                  'Chrome/90.0.4430.93 Safari/537.36'
}
for i in range(5421, 11472):
    url = f'http://www.cfnews.com.cn/toutiao{i}.html'
    try:
        time.sleep(random.random())
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            text = soup.select_one(
                '#main > div > div > div.col-lg > div.row.dd-fie9-2 > div.col-md > div.detail > div.ueditor-content').text
            if len(text) > 10:
                print(i, text)
                with open('../data/corpus/corpus.txt', 'a', encoding='utf-8') as f:
                    print(text.strip('\n'), file=f)
    except:
        continue
# diyixianchang 11435
