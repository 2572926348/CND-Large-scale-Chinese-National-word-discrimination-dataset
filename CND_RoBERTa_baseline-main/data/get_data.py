import json
import random

import pandas as pd
from sqlalchemy import create_engine, text

# 初始化数据库连接
# 按实际情况依次填写MySQL的用户名、密码、IP地址、端口、数据库名
engine = create_engine('mysql+pymysql://root:root@172.19.138.185:3306/Cloze')
results = {}
idiomlist = []
idiom_file = open('idiomList.txt', mode='w')
train_file = open('train_data.txt', mode='a+')
with engine.connect() as conn:
    data = conn.execute(text('select * from cloze'))
    for item in data:
        candidate = item[2].split(',')
        idiomlist.extend(candidate)
        random.shuffle(candidate)
        temp = {"groundTruth": [item[1]], "candidates": [candidate], "content": item[0], "realCount": 1}
        temp = json.dumps(temp, ensure_ascii=False)
        train_file.write(temp + '\n')
idiom_file.write(str(list(set(idiomlist))))
