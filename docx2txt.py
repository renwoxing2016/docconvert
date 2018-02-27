# -*- coding: utf-8 -*-
"""
Created on Mon Feb 26 16:01:33 2018

@author: 
"""
import docconvert_until
import pdfconvert_until
import search_until

# #######################
# #从docx文档中搜索关键字

def search_keyword_from_docx(docpath,keyword):
    # #先把文档转换为文本 list
    doctext = docconvert_until.convert_docx_2_text(docpath)
    
    keycounter = 0
    
    # #循环 文本 list
    for linetxt in doctext:
        if(linetxt == ''):
            continue
        if(linetxt == '\n'):
            continue
        
        # #对每行文本做分词处理
        #fencitxt = search_until.fenci_text(linetxt)
        #print(fencitxt)
        
        # #从每行文本中搜索关键词
        num = search_until.search_first_oflinetxt(keyword,linetxt)
        
        keycounter = keycounter + num
        
    print('keyword count: ',keycounter)
    return keycounter

# #######################
# #从pdf文档中搜索关键字

def search_keyword_from_pdf(pdfpath,keyword):
    keycounter = 0
    
    # #先把文档转换为文本 list
    #doctext = pdfconvert_until.convert_pdf_2_alltext(pdfpath)
    doctext = pdfconvert_until.convert_pdf_2_textlist(pdfpath)
    
    #lenth = len(doctext)
    #print(lenth)
    
    # #循环 文本 list
    for linetxt in doctext:
        if(linetxt == ''):
            continue
        if(linetxt == '\n'):
            continue
        
        # #对每行文本做分词处理
        #fencitxt = search_until.fenci_text(linetxt)
        #print(fencitxt)
        
        # #从每行文本中搜索关键词
        num = search_until.search_first_oflinetxt(keyword,linetxt)
        #print(linetxt)
        #print('find result. ',num)
        #print('--------------------')
        keycounter = keycounter + num
        
    #print('keyword count: ',keycounter)
    return keycounter

# #######################
# #ceshi

#num = search_keyword_from_docx(u'201802-08信息.docx',u'感')

num = search_keyword_from_pdf('项目1.pdf',u'管理')
print('keyword count: ',num)