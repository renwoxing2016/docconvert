# -*- coding: utf-8 -*-
"""
Created on Tue Feb 27 09:57:29 2018

@author: 
"""


import jieba
import re

# #######################
# #针对中文的分词处理

# 分词模式 0精确 1全模式 2搜索模式
FENCI_FLAG = 0

# 分词处理 默认模式 精确模式
def fenci_text(txtcontent):
    refc = ''
    if(FENCI_FLAG == 2):
        refc = text_2_word_search(txtcontent)
    if(FENCI_FLAG == 1):
        refc = text_2_word_cutall(txtcontent)
    else:
        refc = text_2_word_cut(txtcontent)
    return refc

# 用户字典的格式要求:
# 用户字典中每行一个词，格式为：词语 词频 词性
# 其中词频是一个数字，词性为自定义的词性，要注意的是词频数字和空格都要是半角的。
# 如 创新办 5 i

def text_2_word_cut(txtcontent):
    # 使用用户字典
    jieba.load_userdict('user_dict.txt')
    # 精确模式，试图将句子最精确地切开，适合文本分析
    seglist=jieba.cut(txtcontent)
    #print('/'.join(seglist))

    refc = 'output'
    for x in seglist:
        refc = refc + ',' + x
    
    return refc


def text_2_word_cutall(txtcontent):
    # 使用用户字典
    jieba.load_userdict('user_dict.txt')
    # 全模式，把句子中所有的可以成词的词语都扫描出来,速度非常快，但是不能解决歧义
    seglist=jieba.cut(txtcontent,cut_all=True)
    #print('/'.join(seglist))
    
    refc = 'output'
    for x in seglist:
        refc = refc + ',' + x
        
    return refc


def text_2_word_search(txtcontent):
    # 使用用户字典
    jieba.load_userdict('user_dict.txt')
    # 搜索引擎模式，在精确模式的基础上，对长词再次切分，提高召回率，适合用于搜索引擎分词
    seglist=jieba.cut_for_search(txtcontent)
    #print('/'.join(seglist))
    
    refc = 'output'
    for x in seglist:
        refc = refc + ',' + x
    
    return refc

# #######################
# #针对中文的搜索处理 关键词

# #返回在整个字符串的匹配位置
def search_first_oflinetxt(keyword,linetxt):
    parttern = re.compile('.*(%s).*' % keyword)
    # search匹配整个字符串，直到找到一个匹配
    result = re.search(parttern,linetxt)
    
    num = 0
    #num = len(result.groups())
    
    if(result):
        num = 1
        #print(result.group(0)) # #group(0) 匹配的整个字符
        #print(result.group(1)) # #group(1) 匹配的关键字
    else:
        num = 0
        #print('not find')
    return num

def search_all_oflinetxt(keyword,linetxt):
    parttern = re.compile('(%s)' % keyword)
    # 在字符串中找到正则表达式所匹配的所有子串，并返回一个列表，如果没有找到匹配的，则返回空列表
    relist = parttern.findall(linetxt)
    #print(relist)
    
    num = 0
    num = len(relist)
    
    for wd in relist:
        print(wd)
    return num


# #######################
# #ceshi

#retxt = fenci_text(u'阴阳师总是抽不到茨木童子好伤心')
#print('....')
#print(retxt)

#num = search_first_oflinetxt(u'茨木童子',u'阴阳师茨木童子总是抽不到茨木童子好伤心')
#print(num)

#print('....')
#num = search_all_oflinetxt(u'阴阳师',u'阴阳师总是抽不到茨木童子好伤心 阴阳师是茨木童子好')
#print(num)


