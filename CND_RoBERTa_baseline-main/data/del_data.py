import csv
import pandas as pd
with open('idiomList.txt',encoding='utf-8') as f:
    line=f.readline()
    line=eval(line)
    idiom_num={}
    for i in line:
        idiom_num[i]=0
tsvreader=pd.read_csv("Cloze_final_cloze.csv")
for index,row in tsvreader.iterrows() :
    idiom_num[row['truth']]+=1
print(idiom_num)

a = dict(sorted(idiom_num.items(), key=lambda x: x[1]))
print(a)