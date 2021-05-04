import base64
import json
import logging
import os
import re

import cv2
import jieba
import pandas as pd
import requests
from gensim.models import Word2Vec

import config

jieba.setLogLevel(logging.INFO)


# 调用百度api识别图片
class Identify:
    def __init__(self, filepath):
        # 判断路径是否存在
        if not os.path.exists(filepath):
            raise FileNotFoundError("Path doesn't exist.")
        self.filepath = filepath
        with open(filepath, 'rb') as f:
            self.img = base64.b64encode(f.read())
        with open(config.token) as f:
            self.tokens = json.load(f)

    def __call__(self):
        self.main_object_location = self.get_api_image_object_detect()["result"]
        self.cut_image()
        self.main_object_identify = self.get_api_image_advanced_general()
        self.main_text = self.get_api_text_accurate_basic()
        _, img, wd = self.main_object_location, self.main_object_identify, self.main_text
        img, wd = image_filter(img), word_filter(wd)
        # print(img[0] + ''.join(wd))
        return img[0] + ''.join(wd)

    def cut_image(self):
        # 图像主体位置识别
        y0 = self.main_object_location["top"]
        y1 = y0 + self.main_object_location["height"]
        x0 = self.main_object_location["left"]
        x1 = x0 + self.main_object_location["width"]
        # 裁剪并保存
        image = cv2.imread(self.filepath)
        cropped = image[y0:y1, x0:x1]  # 裁剪坐标为[y0:y1, x0:x1]
        filename = os.path.basename(self.filepath)
        cropped_path = os.path.join(config.Cimage, "cut_" + filename)
        cv2.imwrite(cropped_path, cropped)
        with open(cropped_path, "rb") as f:
            self.img = base64.b64encode(f.read())

    def get_api_image_advanced_general(self):
        request_url = "https://aip.baidubce.com/rest/2.0/image-classify/v2/advanced_general"

        params = {"image": self.img}
        access_token = self.tokens["img"]["token"]
        request_url = request_url + "?access_token=" + access_token
        headers = {'content-type': 'application/x-www-form-urlencoded'}
        return self._post(request_url, params, headers)

    def get_api_image_object_detect(self):
        request_url = "https://aip.baidubce.com/rest/2.0/image-classify/v1/object_detect"

        params = {"image": self.img, "with_face": 1}
        access_token = self.tokens["img"]["token"]
        request_url = request_url + "?access_token=" + access_token
        headers = {'content-type': 'application/x-www-form-urlencoded'}
        return self._post(request_url, params, headers)

    def get_api_text_accurate_basic(self):
        request_url = "https://aip.baidubce.com/rest/2.0/ocr/v1/accurate_basic"

        params = {"image": self.img}
        access_token = self.tokens["word"]["token"]
        request_url = request_url + "?access_token=" + access_token
        headers = {'content-type': 'application/x-www-form-urlencoded'}
        return self._post(request_url, params, headers)

    @staticmethod
    def _post(request_url, params, headers):
        response = requests.post(request_url, data=params, headers=headers)
        if response:
            return response.json()


# 图片结果处理
def image_filter(img_results):
    keywords = []
    for result in img_results['result']:
        # if not result['root'].startswith('商品'):
        #     continue
        keywords.append(result['keyword'])
    return keywords


# ocr文字结果处理
def word_filter(word_results):
    results = []
    for result in word_results['words_result']:
        results.append(result['words'])
    return results


# 将识别结果分词 分类
def categorize(result):
    pattern = re.compile(r'[\sA-Za-z～()（）【】%*#+\-.\\/:=：_,，。、;；“”"\'’‘？?！!<《》>^&{}|…]')
    result = re.sub(pattern, '', result)
    cut_list = jieba.lcut(result, cut_all=False)
    # print(cut_list)
    model = Word2Vec.load(config.model)
    ck_list = ['苹果', '牛奶', '花蛤', '黄瓜', '牛肉丸', '矿泉水', '花生', '白糖',
               '绿茶', '柿子', '排骨', '蜂蜜', '麻花', '花生油', '罐头', '豆腐干',
               '白菜', '雪糕', '米粉', '粉条', '鸡蛋', '鸡肉', '软糖', '粉条', '奶粉',
               '生菜', '饼干', '蛋糕', '白酒', '燕麦片', '大米', '酱油', '薯片', '章鱼']  # 每类选出代表词
    scores = []
    idx = []
    for word in cut_list:
        ck_word = []
        for ck in ck_list:
            try:
                smlty = model.wv.similarity(word, ck)
            except:
                smlty = 0
            ck_word.append(smlty)
        max_score = max(ck_word)
        scores.append(max_score)
        max_index = ck_word.index(max_score)
        idx.append(max_index)
    mx_score = max(scores)
    # print(mx_score)
    if mx_score < 0.85:
        return None, None
    mx_id = scores.index(mx_score)

    return cut_list[mx_id], idx[mx_id]


# 展示结果
def show(raw_result, category):
    if category is None:
        print('--------------------------------------------------------------------------')
        print('未识别到结果，请将镜头对准食品！')
    else:
        df = pd.read_csv(config.uq_rate, index_col=0)
        # print(category)
        df = df.loc[category]
        # print(df)
        print('--------------------------------------------------------------------------')
        print('识别成功！')
        print(f'识别结果：{raw_result}')
        print(f'食品类别：{config.id2label[category]}')
        print(f'抽检不合格数：{int(df["unqualified_num"])}')
        print(f'抽检总数：{int(df["check_num"])}')
        print(f'抽检不合格率：{df["uq_rate"]}')


if __name__ == '__main__':
    show(*categorize('梨'))
