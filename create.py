# -*- coding: UTF-8 -*-
import caffe
import os
from caffe.proto import caffe_pb2
import lmdb
import random
import numpy as np

def make_datum(img, label):
    #image is numpy.ndarray format. BGR instead of RGB
    return caffe_pb2.Datum(
        channels=3,
        width=16,
        height=1,
        label=label,
        data=img.tobytes())


if __name__=='__main__':
    train_data=open('F:/111/111/train_data.csv').readlines()
    labels=open('F:/111/111/labels.csv').readlines()
    in_db=lmdb.open("F:/111/111/train_lmdb", map_size=30000000)

    with in_db.begin(write=True) as in_txn:
        index=0
        for train in train_data:
            data=train.split(',')[:-1]
            data=np.mat(data)

            datum = make_datum(data, int(labels[index]))

            # '{:0>5d}'.format(in_idx):
            #      lmdb的每一个数据都是由键值对构成的,
            #      因此生成一个用递增顺序排列的定长唯一的key
            in_txn.put('{:0>5d}'.format(index), datum.SerializeToString())  # 调用句柄，写入内存
            print index
            index+=1

    # 结束后记住释放资源，否则下次用的时候打不开。。。
    in_db.close()



