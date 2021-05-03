# -*- encoding: utf-8 -*-
# @Time      : 2021/4/22 16:22
# @Author    : zzh
# @File      : model.py

import re

import jieba
from gensim.models.word2vec import LineSentence
from gensim.models.word2vec import Word2Vec
import config


class TrainWord2Vec:
    """
    训练Word2Vec模型
    """

    def __init__(self, corpus=config.corpus, corpus_cut=config.corpus_cut, stopword=config.stopword,
                 num_features=100, min_word_count=1, context=4, incremental=False,
                 old_path="word2vec.model"):
        """
        定义变量
        :param corpus: 用于训练的语料
        :param corpus_cut: 分词过的语料
        :param stopword: 停用词表
        :param num_features:  返回的向量长度
        :param min_word_count:  最低词频
        :param context: 滑动窗口大小
        :param incremental: 是否进行增量训练
        :param old_path: 若进行增量训练，原始模型路径
        """
        self.corpus = corpus
        self.corpus_cut = corpus_cut
        self.stopword = [word.strip('\n') for word in open(stopword, encoding='utf-8')]
        print(self.stopword)
        self.num_features = num_features
        self.min_word_count = min_word_count
        self.context = context
        self.incremental = incremental
        self.old_path = old_path

    def clean_text(self):
        # 读取文件内容到列表
        fileTrainRead = []
        with open(self.corpus, 'r', encoding='utf-8') as fileTrainRaw:
            for line in fileTrainRaw:  # 按行读取文件
                fileTrainRead.append(line)

        # jieba分词后保存在列表中
        fileTrainSeg = []
        for i, line in enumerate(fileTrainRead):
            pattern = re.compile(r'[\sA-Za-z～()（）【】%*#+\-.\\/:=：_,，。、;；“”"\'’‘？?！!<《》>^&{}|…]')
            line = re.sub(pattern, '', line)
            cut_list = jieba.lcut(line, cut_all=False)
            cut_word = [word for word in cut_list if word not in self.stopword]
            fileTrainSeg.append(' '.join(cut_word))
            if i % 100 == 0:
                print(i)

        # 保存分词结果到文件中
        with open(self.corpus_cut, 'w', encoding='utf-8') as fW:
            for line in fileTrainSeg:
                fW.write(line)
                fW.write('\n')
        return self.corpus_cut

    def get_model(self, text=config.corpus_cut):
        """
        从头训练word2vec模型
        :param text: 经过清洗之后的语料数据
        :return: word2vec模型
        """
        model = Word2Vec(LineSentence(text), size=self.num_features, min_count=self.min_word_count, window=self.context)
        return model

    def update_model(self, text):
        """
        增量训练word2vec模型
        :param text: 经过清洗之后的新的语料数据
        :return: word2vec模型
        """
        model = Word2Vec.load(self.old_path)  # 加载旧模型
        model.build_vocab(text, update=True)  # 更新词汇表
        model.train(text, total_examples=model.corpus_count,
                    epochs=model.iter)  # epoch=iter语料库的迭代次数；（默认为5）  total_examples:句子数。
        return model

    def main(self):
        """
        主函数，保存模型
        """
        # 加入自定义分析词库
        # jieba.load_userdict("add_word.txt")
        text = self.clean_text()
        if self.incremental:
            model = self.update_model(text)
        else:
            model = self.get_model(text)
        # 保存模型
        model.save(config.model)


if __name__ == '__main__':
    # trainmodel = TrainWord2Vec()
    # trainmodel.main()
    model = Word2Vec.load(config.model)
    # model.wv.save_word2vec_format('word2vec.vector')
    # print(model.wv.similar_by_word("猪肉"))
    print(model.similarity('苹果', '香蕉'))
    print(model.most_similar('奶'))
