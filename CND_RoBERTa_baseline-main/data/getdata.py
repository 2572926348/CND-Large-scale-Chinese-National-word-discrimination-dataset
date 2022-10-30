import pandas as pd
import numpy as np
import json
import csv
import random
import tqdm
import sys, time
# 合并
# f1 = pd.read_csv('1.csv')
# print(f1)
# f2 = pd.read_csv('Cloze_final_cloze.csv')
# print(f2)
# file = [f1,f2]
# train = pd.concat(file,axis=1)
# train.to_csv("cloze_final" + ".csv", index=0, sep=',')
# print('合并完成')
class ShowProcess():
    """
    显示处理进度的类
    调用该类相关函数即可实现处理进度的显示
    """
    i = 0 # 当前的处理进度
    max_steps = 0 # 总共需要处理的次数
    max_arrow = 50 #进度条的长度
    infoDone = 'done'

    # 初始化函数，需要知道总共的处理次数
    def __init__(self, max_steps, infoDone = 'Done'):
        self.max_steps = max_steps
        self.i = 0
        self.infoDone = infoDone

    # 显示函数，根据当前的处理进度i显示进度
    # 效果为[>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>]100.00%
    def show_process(self, i=None):
        if i is not None:
            self.i = i
        else:
            self.i += 1
        num_arrow = int(self.i * self.max_arrow / self.max_steps) #计算显示多少个'>'
        num_line = self.max_arrow - num_arrow #计算显示多少个'-'
        percent = self.i * 100.0 / self.max_steps #计算完成进度，格式为xx.xx%
        process_bar = '[' + '>' * num_arrow + '-' * num_line + ']'\
                      + '%.2f' % percent + '%' + '\r' #带输出的字符串，'\r'表示不换行回到最左边
        sys.stdout.write(process_bar) #这两句打印字符到终端
        sys.stdout.flush()
        if self.i >= self.max_steps:
            self.close()

    def close(self):
        print('')
        print(self.infoDone)
        self.i = 0
if __name__ == '__main__':

    idiomlist = []
    # idiom_file = open('idiomList.txt', mode='w', encoding='utf-8')
    train_file = open('train_data.txt', mode='a+', encoding='utf-8')
    val_file = open('dev_data.txt', mode='a+', encoding='utf-8')
    test_file = open('test_data.txt', mode='a+', encoding='utf-8')

    tsvreader = pd.read_csv('Cloze_final_cloze.csv')
    # with open('Cloze_final_cloze.csv',encoding="utf-8",) as f:
    #     next(f)
    #     tsvreader = csv.reader(f)
    max_steps = 100
    process_bar = ShowProcess(max_steps, 'OK')
    for index,row in tsvreader.iterrows():
        process_bar.show_process()
        candidate = row['candidate'].split(',')
        candidate = [i for i in candidate if i != ""]
        temp = [row['truth']]
        candidate.remove(row['truth'])
        temp.append(candidate[0])
        temp = list(set(temp))
        random.shuffle(temp)

        assert len(temp) == 2
        idiomlist.extend(candidate)
        temp = {"groundTruth": [row['truth']], "candidates": [temp], "content": row['content'], "realCount": 1}
        temp = json.dumps(temp, ensure_ascii=False)
        p = np.random.uniform()
        if p <= 0.1:
            val_file.write(temp + '\n')
        if p > 0.1 and p < 0.3:
            test_file.write(temp + '\n')
        if p >= 0.3:
            train_file.write(temp + '\n')
    # idiom_file.write(str(list(set(idiomlist))))

    train_file = open('train_data.txt',encoding='utf-8')
    test_file = open('test_data.txt',encoding='utf-8')
    val_file = open('dev_data.txt',encoding='utf-8')
    lines1 = len(train_file.readlines())
    lines2 = len(test_file.readlines())
    lines3 = len(val_file.readlines())
    print(lines1, lines2, lines3)
