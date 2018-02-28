# -*- coding: utf-8 -*-
"""
Created on Mon Feb 26 16:00:44 2018

@author: 
"""
# #######################
# #此处理包括如下几种文件转换
# #pdf --> txt
# #pdf --> jpg
# #
# #http://blog.csdn.net/fighting_no1/article/details/51038942

# #######################
# #此处理 pdf --> txt
from io import open
from io import StringIO
#from cStringIO import StringIO

from pdfminer.pdfparser import PDFParser, PDFDocument, PDFNoOutlines
#from pdfminer.pdfpage import PDFPage
from pdfminer.pdfdevice import PDFDevice

from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter, process_pdf
from pdfminer.converter import TextConverter, PDFPageAggregator
from pdfminer.layout import LAParams, LTTextBoxHorizontal

from pdfminer.pdfinterp import PDFTextExtractionNotAllowed

# #解析pdf后把所有文本输出
# #一次性返回的pdf内的所有文本
def readPDF(pdfFile):
    rsrcmgr = PDFResourceManager()
    retstr = StringIO()
    laparams = LAParams()
    device = TextConverter(rsrcmgr, retstr, laparams=laparams)
    
    process_pdf(rsrcmgr, device, pdfFile)
    device.close() 
    
    content = retstr.getvalue()
    retstr.close()
    
    return content 

# #解析pdf后把每页的文本输出
# #返回的文本list 每个表示的是每页的文本
def parsePDF(pdfFile):
    # 以二进制读模式打开
    fp = open(pdfFile, 'rb')
    #用文件对象来创建一个pdf文档分析器
    praser = PDFParser(fp)
    
    # 创建一个PDF文档
    doc = PDFDocument()
    # 连接分析器 与文档对象
    praser.set_document(doc)
    doc.set_parser(praser)
    
    # 文本的list
    textlist = ['.']
    
    # 提供初始化密码
    # 如果没有密码 就创建一个空的字符串
    doc.initialize()
    
    # 检测文档是否提供txt转换，不提供就忽略
    if not doc.is_extractable:
        # raise PDFTextExtractionNotAllowed
        return None
    else:
        # 创建PDf 资源管理器 来管理共享资源
        rsrcmgr = PDFResourceManager()
        # 创建一个PDF设备对象
        laparams = LAParams()
        device = PDFPageAggregator(rsrcmgr, laparams=laparams)
        # 创建一个PDF解释器对象
        interpreter = PDFPageInterpreter(rsrcmgr, device)

        # 循环遍历列表，每次处理一个page的内容
        # doc.get_pages() 获取page列表
        for page in doc.get_pages():
            # 接受该页面的LTPage对象
            interpreter.process_page(page)
            # 这里layout是一个LTPage对象 里面存放着 这个page解析出的各种对象 
            # 一般包括LTTextBox, LTFigure, LTImage, LTTextBoxHorizontal 等等
            # 想要获取文本就获得对象的text属性，
            layout = device.get_result()
            
            for x in layout:
                if (isinstance(x, LTTextBoxHorizontal)):
                    # with open(r'../../data/pdf/1.txt', 'a') as f:
                    #     results = x.get_text()
                    #     print(results)
                    #     f.write(results + '\n')
                    results = x.get_text()
                    #print(results)
                    #print('---------------------------')
                    textlist.append(results)
        
        device.close()
        
    return textlist


# #取得pdf的目录
# #返回的目录及对应的主题文本
def getindex_of_PDF(pdfFile):
    fp = open(pdfFile, 'rb')
    #用文件对象来创建一个pdf文档分析器
    praser = PDFParser(fp)
    
    # 创建一个PDF文档
    document = PDFDocument()
    # 连接分析器 与文档对象
    praser.set_document(document)
    document.set_parser(praser)
    # 提供初始化密码
    # 如果没有密码 就创建一个空的字符串
    document.initialize()

    lvllist = ''
    titlelist = ''

    if(document.catalog == None):
        return lvllist,titlelist
    
    # .获得文档的目录（纲要）
    try:
        pdfoutlines = document.get_outlines()
    except (PDFNoOutlines):
        print('pdf no Outlines..')
        return lvllist,titlelist
    
    for (level,title,dest,a,se) in pdfoutlines:
        print(level, title)
        lvllist.append(str(level))
        titlelist.append(title)
    
    fp.close()
    
    return lvllist,titlelist


# #返回的文本list 每个表示的是每页的文本
def convert_pdf_2_textlist(pdfpath):
    textlist = parsePDF(pdfpath)
    
    return textlist

# #一次性返回的pdf内的所有文本
def convert_pdf_2_alltext(pdfpath):
    # #有的pdf解析时出现PDFEncryptionError: Unknown algorithm
    # #表明此pdf文件有密码，但密码是空字符串，所以必须要解密一下才可以做解析，如下处理
    #from subprocess import call
    # pdf_filename代表源文件路径， pdf_copy_filename代表解密后的文件路径， 密码为''
    #call('qpdf --password=%s --decrypt %s %s' % ('', pdf_filename, pdf_copy_filename), shell=True)
    
    pdffile = open(pdfpath, 'rb')
    text = readPDF(pdffile)
    
    # #如下写入的是十六进制 不是希望的结果
    # txtfile = open(txtpath,'a')
    # txtfile.write(str(text.encode('utf-8')+b"\n"))
    
    pdffile.close()
    return text

def convert_pdf_save_text(pdfpath,txtpath):
    # #有的pdf解析时出现PDFEncryptionError: Unknown algorithm
    # #表明此pdf文件有密码，但密码是空字符串，所以必须要解密一下才可以做解析，如下处理
    #from subprocess import call
    # pdf_filename代表源文件路径， pdf_copy_filename代表解密后的文件路径， 密码为''
    #call('qpdf --password=%s --decrypt %s %s' % ('', pdf_filename, pdf_copy_filename), shell=True)
    
    pdffile = open(pdfpath, 'rb')
    text = readPDF(pdffile)
    pdffile.close()
    
    # #如下写入的是十六进制 不是希望的结果
    # txtfile = open(txtpath,'a')
    # txtfile.write(str(text.encode('utf-8')+b"\n"))
    
    # #如下写入的是中文
    txtfile = open(txtpath,'wb+')
    txtfile.write(text.encode('utf-8'))
    txtfile.close()
    
    return text

# #######################
# #此处理 pdf中的图片 --> jpg
import PythonMagick
from PyPDF2 import PdfFileReader
 
C_JPGNAME=r'pdf_%s.jpg';

def convert_imageofpdf_2_jpg(pdfpath,jpgpath):
    input_stream = open(pdfpath, 'rb')
    pdf_input = PdfFileReader(input_stream,strict=False) # 获取一个 PdfFileReader 对象 
    page_count = pdf_input.getNumPages() # 获取 PDF的页数 
    print('page numbers. ',page_count)
    #img = PythonMagick.Image()   # empty object first
    #img.density('300')           # set the density for reading (DPI); must be as a string
    
    for i in range(page_count):
        print('done.',i)
        #img.read(pdfpath + '[' + str(i) +']')     #分页读取 PDF
        #imgCustRes = PythonMagick.Image(img)  # make a copy
        #imgCustRes.sample('x1600')
        #imgCustRes.write(jpgpath+'/'+(C_JPGNAME%i))
        imgCustRes = PythonMagick.Image(pdf_input.getPage(i))
        #imgCustRes = PythonMagick.Image(pdfpath + '[' + str(i) +']')  # 分页读取 PDF
        imgCustRes.density('300')
        imgCustRes.write(jpgpath+'/'+'pdf_1.jpg')
    
    print('all done')
    return page_count

# #######################
# #ceshi

#convert_pdf_2_text('项目1.pdf','b.txt')

#C_RESOURCE_FILE=r'G:/temp/tf/docconvert';
#convert_imageofpdf_2_jpg(u'G:/temp/tf/docconvert/项目1.pdf',C_RESOURCE_FILE) #ng

#indexl,indextitle = getindex_of_PDF('项目1.pdf')
indexl,indextitle = getindex_of_PDF('工业大数据白皮书2017.pdf')
print(indexl)
print(indextitle)

