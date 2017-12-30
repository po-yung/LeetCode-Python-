# -*- coding: utf-8 -*-
"""
Created on Tue Dec 26 11:01:37 2017

@author: 45543
"""
import pandas as pd
import os

os.chdir('C:\\Users\\45543\\Desktop\\02-Data')
data = pd.read_csv('comment.csv', encoding = 'utf-8')

data.品牌.value_counts()
comment = data[data.品牌 == 'AO']
comment = comment.评论
# 机械压缩（自定义函数实现，并统计压缩前后评论总字数的变化情况）
def yasuo(str1):
    # 一字词、两字词（重复两次或以上）
    #str1 = '奖项在嘉兴嘉兴嘉兴'
    str1 = str(str1)
    for i in [1,2]:
        for j in range(len(str1) - 2*i):
            if str1[j:j+i] == str1[j+i:j+2*i] and str1[j+i:j+2*i] == str1[j+2*i:j+3*i]:
                k = j + 2*i
                while k + 2*i <= len(str1) and str1[k+i:k+2*i] == str1[j:j+i]:
                    k += i
                str1 = str1[:j] + str1[k:]
    # 三字词及以上（重复一次或以上）
    #str1 = '谁不说咱家乡家乡家乡家乡家乡美谁不说咱家乡家乡家乡家乡家乡美'
    for i in range(3, int(len(str1)/2) + 1):
        for j in range(len(str1) - i):
            if str1[j:j+i] == str1[j+i:j+2*i]:
                k = j + i
                while k + i <= len(str1) and str1[k+i:k+2*i] == str1[j:j+i]:
                    k += i
                str1 = str1[:j] + str1[k:]
    return(str1)

# 测试自定义函数
yasuo('谁不说咱家乡家乡家乡家乡家乡美')
yasuo('谁不说咱家乡家乡家乡家乡家乡美谁不说咱家乡家乡家乡家乡家乡美')
yasuo('滔滔不绝')
yasuo('滔滔不绝滔滔不绝')
# 统计机械压缩前的字符总数
n1 = comment.astype(str).apply(lambda x: len(x)).sum()
# 对comment进行机械压缩
comment1 = comment.apply(lambda x: yasuo(x))
# 统计机械压缩后的字符总数
n2 = comment1.astype(str).apply(lambda x: len(x)).sum()
print('机械压缩共减少%d个字符'%(n1-n2))

# 1 热水器型号——删除：AO史密斯（A.O.Smith） ET300J-50 电热水器 50升
temp = data[data.品牌 == 'AO']
temp.型号.value_counts()
del temp
import re
patten = re.compile('AO史密斯（A.O.Smith） ET.00J-.0 电热水器 .0升')
comment2 = comment1.astype(str).apply(lambda x: patten.sub('', x))
n3 = comment2.astype(str).apply(lambda x: len(x)).sum()
# 2 表情符号、换行符号、空格——删除：&hellip;| |\n
comment3 = pd.Series([re.sub(r'&[a-z]+;| |\\n','',
                             comment2[i]) for i in comment.index])
n4 = comment3.astype(str).apply(lambda x: len(x)).sum()
n3-n4
# 3 短句删除(字符串长度小于等于4的——删除)
num = pd.Series([len(comment3[i]) for i in comment3.index])
data1 = pd.concat([comment3, num], axis = 1)
data2 = data1[data1[1] > 4]
coment4 = data2[0]
del data1,data2

# 4 去重
comment4 = coment4.drop_duplicates()

# 分词
import jieba
cut_com = comment4.apply(lambda x: jieba.lcut(x))

# 去除停用词
stop = pd.read_csv('stoplist.txt', header = None, 
                   sep = 'yang',
                   encoding = 'utf-8')
stop = [' '] + list(stop[0])
cut_com1 = cut_com.apply(lambda x:[i for i in x if i not in stop])
cut_com1.astype(str).apply(lambda x:len(x)).sum()
cut_com.astype(str).apply(lambda x:len(x)).sum()

def cipin(after_cut, num):
#    after_cut = cut_com1.copy()
#    num = 5
    a = [' '.join(after_cut[i]) for i in after_cut.index]
    b = ' '.join(a)
    h = pd.Series(b.split())
    dat = h.value_counts()
    dat1 = dat[dat >= num]
    return dat1
    
cut_num = cipin(cut_com1, 20)
from scipy.misc import imread
from wordcloud import WordCloud
import matplotlib.pyplot as plt
back_pic = imread("C:\\Users\\45543\\Desktop\\aixin.jpg")  # 设置背景图片  
wc = WordCloud( font_path='C:\\Windows\\Fonts\\simkai.TTF',#设置字体  
                background_color="white", #背景颜色  
                max_words=2000,# 词云显示的最大词数  
                mask=back_pic,#设置背景图片  
                max_font_size=200, #字体最大值  
                random_state=42,  
                )
gar_wordcloud = wc.fit_words(cut_num)  # cut_num是由频数构成的Series的形式，且单词作为索引
plt.figure(figsize=(16,8))
plt.imshow(gar_wordcloud)
plt.axis('off') 
plt.show()
wc.to_file(path.join(d, “ciyun.png")) # 保存图片  







