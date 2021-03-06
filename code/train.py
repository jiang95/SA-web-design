#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @author : lingjun.jlj
# @create : 2018/3/2

import sys

reload(sys)
sys.setdefaultencoding('utf8')
import nltk
import numpy as np
from keras.preprocessing import sequence
from sklearn.model_selection import train_test_split

from code.Vocabulary import load_data
from utils.constant import *
from utils.lstm_train import make_model


def word_to_index(maxlen, num_recs, word_freqs):
    # 文本转为索引数字模式
    with open(path + 'data/train_data.txt', 'r+') as f:
        for line in f:
            label, sentence = line.strip().split("\t")
            words = nltk.word_tokenize(sentence.lower())
            if len(words) > maxlen:
                maxlen = len(words)
            for word in words:
                word_freqs[word] += 1
            num_recs += 1
    data = load_data(12499, 12499)
    # 另一份数据
    for sentence, label in data:

        words = nltk.word_tokenize(sentence.decode('utf-8').lower())
        if len(words) > maxlen:
            maxlen = len(words)
        for word in words:
            word_freqs[word] += 1
        num_recs += 1

    print('max_len ', maxlen)
    print('nb_words ', len(word_freqs))

    # 准备数据
    MAX_FEATURES = 2000
    vocab_size = min(MAX_FEATURES, len(word_freqs)) + 2
    word2index = {x[0]: i + 2 for i, x in enumerate(word_freqs.most_common(MAX_FEATURES))}
    word2index["PAD"] = 0
    word2index["UNK"] = 1
    return word2index, vocab_size, num_recs, word_freqs


def train():
    nltk.download('punkt')
    maxlen = 0  # 句子最大长度
    num_recs = 0  # 样本数
    word_freqs = collections.Counter()  # 词频
    word2index, vocab_size, num_recs, word_freqs = word_to_index(maxlen, num_recs, word_freqs)

    X = np.empty(num_recs, dtype=list)
    y = np.zeros(num_recs)
    i = 0

    with open(path + 'data/train_data.txt', 'r+') as f:
        for line in f:
            label, sentence = line.strip().split("\t")
            words = nltk.word_tokenize(sentence.lower())
            seqs = []
            for word in words:
                if word in word2index:
                    seqs.append(word2index[word])
                else:
                    seqs.append(word2index["UNK"])
            X[i] = seqs
            y[i] = int(label)
            i += 1

    data = load_data(12499, 12499)
    for sentence, label in data:
        words = nltk.word_tokenize(sentence.decode('utf-8').lower())
        seq = []
        for word in words:
            if word in word2index:
                seq.append(word2index[word])
            else:
                seq.append(word2index["UNK"])
        X[i] = seq
        y[i] = int(label)
        i += 1

    X = sequence.pad_sequences(X, maxlen=MAX_SENTENCE_LENGTH)

    # 数据划分 80% 作为训练数据，20% 作为测试数据
    Xtrain, Xtest, Ytrain, Ytest = train_test_split(X, y, test_size=0.2, random_state=42)

    # 训练模型
    model = make_model(vocab_size, Xtrain, Ytrain, Xtest, Ytest)

    model.save(path + 'data/train_model.h5')

    print "训练结束"


if __name__ == '__main__':
    train()
