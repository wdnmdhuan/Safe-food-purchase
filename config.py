import datetime
import os

base_dir = 'data'

image_dir = os.path.join(base_dir, 'images')
Cimage = os.path.join(image_dir, 'Cimage')
Oimage = os.path.join(image_dir, 'Oimage')
Timage = os.path.join(image_dir, 'Timage')

corpus_dir = os.path.join(base_dir, 'corpus')
stopword = os.path.join(base_dir, 'stopword.txt')
label = os.path.join(corpus_dir, 'labels.txt')
foodsec = os.path.join(corpus_dir, 'foodsec.csv')
corpus = os.path.join(corpus_dir, 'corpus.txt')
corpus_cut = os.path.join(corpus_dir, 'corpus_cut.txt')
uq_rate = os.path.join(corpus_dir, 'uq_rate.csv')

model = os.path.join(base_dir, 'model', 'word2vec.model')

now = datetime.datetime.now()
now = now - datetime.timedelta(microseconds=now.microsecond)
zero_tomorrow = now - datetime.timedelta(days=-1,
                                         hours=now.hour,
                                         minutes=now.minute,
                                         seconds=now.second,
                                         microseconds=now.microsecond)

# timer的启动时间
start = {
    "delete_expired_images": zero_tomorrow,
    "get_token": zero_tomorrow,
    "seeImage": now,
    "test": now,
}

# timer的间隔时间
sleep = {
    "delete_expired_images": {
        "days": 1,
    },
    "get_token": {
        "days": 29,
    },
    "seeImage": {
        "seconds": 5,
    },
    "test": {
        "seconds": 2,
    },
}

id2label = {0: '水果制品', 1: '乳制品', 2: '水产品及水产制品', 3: '蔬菜制品', 4: '速冻食品', 5: '饮料', 6: '炒货食品及坚果制品', 7: '食糖', 8: '茶叶及相关制品',
            9: '水果及其制品', 10: '餐饮食品', 11: '蜂产品', 12: '可可及焙烤咖啡产品', 13: '食用油、油脂及其制品', 14: '罐头', 15: '豆制品', 16: '食用农产品',
            17: '冷冻饮品', 18: '特殊膳食食品', 19: '淀粉及淀粉制品', 20: '蛋制品', 21: '肉制品', 22: '糖果制品', 23: '粮食及粮食制品', 24: '婴幼儿配方食品',
            25: '蔬菜及其制品', 26: '饼干', 27: '糕点', 28: '酒类', 29: '方便食品', 30: '粮食加工品', 31: '调味品', 32: '薯类和膨化食品', 33: '水产制品'}
label2id = {'水果制品': 0, '乳制品': 1, '水产品及水产制品': 2, '蔬菜制品': 3, '速冻食品': 4, '饮料': 5, '炒货食品及坚果制品': 6, '食糖': 7, '茶叶及相关制品': 8,
            '水果及其制品': 9, '餐饮食品': 10, '蜂产品': 11, '可可及焙烤咖啡产品': 12, '食用油、油脂及其制品': 13, '罐头': 14, '豆制品': 15, '食用农产品': 16,
            '冷冻饮品': 17, '特殊膳食食品': 18, '淀粉及淀粉制品': 19, '蛋制品': 20, '肉制品': 21, '糖果制品': 22, '粮食及粮食制品': 23, '婴幼儿配方食品': 24,
            '蔬菜及其制品': 25, '饼干': 26, '糕点': 27, '酒类': 28, '方便食品': 29, '粮食加工品': 30, '调味品': 31, '薯类和膨化食品': 32, '水产制品': 33}
