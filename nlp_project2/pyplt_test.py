# -*- coding: utf-8 -*-
"""
Created on Mon Sep  9 14:50:40 2019

@author: K
"""
# -*- coding: utf-8 -*-
"""
Created on Mon Aug 12 16:12:05 2019

@author: K
"""
# -*- coding: utf-8 -*-
from pyltp import Segmentor#分词
from pyltp import SentenceSplitter# 分句
'''
from pyltp import Postagger  #词性测试
from pyltp import NamedEntityRecognizer #NER
from pyltp import Parser#依存分析
'''
    

class HIT():
    def __init__(self,sentence,): 
        self.sentence=sentence
    
    def sentence_splitter(self):
        sents = SentenceSplitter.split(self.sentence)  # 分句 
        #print('分句子的结果是') 
        #print ('\n'.join(sents)) 
        self.sents=list(sents)
        return self.sents
    
    def segmentor(self):
        segmentor = Segmentor()  # 初始化实例
        ldir='C:\\Users\\K\\ltp_data_v3.4.0\\cws.model'
        dicdir='C:\\Users\\K\\ltp_data_v3.4.0\\word.txt' # 自定义字典
        #segmentor.load('C:\\Users\\K\\ltp_data_v3.4.0\\cws.model')  # 加载模型
        segmentor.load_with_lexicon(ldir, dicdir)
        words = segmentor.segment(self.sentence)  # 分词
        #默认可以这样输出
        #print ('\t'.join(words) )
        # 可以转换成List 输出
        words_list = list(words)
        #print('\n')
        #print ('分词的结果是:')
        #for word in words_list:
         #  print (word,end=' ')
        
        segmentor.release()  # 释放模型 
        self.words=words_list
        return self.words
    ''''
    
    def posttagger(self):
        postagger = Postagger() # 初始化实例
        postagger.load('C:\\Users\\K\\ltp_data_v3.4.0\\pos.model')  # 加载模型
       
        postags = postagger.postag(self.words)  # 词性标注  
        print('\n')
        print('词性标记的结果是')
        
        for word,tag in zip(self.words,postags): 
            
           print (word+'/'+tag)
        postagger.release()  # 释放模型
        self.postags=list(postags)
        return   self.postags

      
  
   
    def ner(self): 
        recognizer = NamedEntityRecognizer() # 初始化实例
        recognizer.load("C:\\Users\\K\\ltp_data_v3.4.0\\ner.model")  # 加载模型
        netags = recognizer.recognize(self.words, self.postags)  # 命名实体识别
        print('\n')
        print('命名实体识别结果是： ')
        for word, ntag in zip(self.words, netags):
            print (word + '/' + ntag)
        recognizer.release()  # 释放模型 
        self.netags= netags 
        return list(self.netags)
    
   
    def parse(self):
        parser = Parser() # 初始化实例
        parser.load('C:\\Users\\K\\ltp_data_v3.4.0\\parser.model')  # 加载模型
        self.arcs = parser.parse(self.words, self.postags)  # 句法分析 
        print('\n')
        print('依存分析结果是： ')
        i=0
        while i<len(self.words):
            
            print ("\t".join("%d:%s" % (arc.head, arc.relation)  for arc in self.arcs))
            self.parse_result=[[arc.head, arc.relation] for arc in self.arcs]
            i+=1
        parser.release()  # 释放模型 
        return self.arcs ,  self.parse_result 
 

if __name__ == "__main__":
   # sentence= "贵州财经大学要举办大数据比赛吗？那让欧几里得去问问看吧！其实是在贵阳花溪区吧。"
    #sentence = """台湾工业总会指出，2015年的白皮书就特别提到台湾面临“五缺”（缺水、缺电、缺工、缺地、缺人才）困境，使台湾整体投资环境走向崩坏。然而四年过去，“五缺”未见改善，反而劳动法规日益僵化、两岸关系陷入紧张、对外关系更加孤立。该团体质疑，台当局面对每年的建言，“到底听进去多少，又真正改善了几多”？"""
   
    model= HIT(sentence)
    model.sentence_splitter()
    model.segmentor()
    model.posttagger()
    model.ner()
    model.parse()
    

     sentence = """
台湾工业总会是岛内最具影响力的工商团体之一，2008年以来，该团体连续12年发表对台当局政策的建言白皮书，集中反映岛内产业界的呼声。\
台湾工业总会指出，2015年的白皮书就特别提到台湾面临“五缺”（缺水、缺电、缺工、缺地、缺人才）困境，使台湾整体投资环境走向崩坏。然而四年过去，“五缺”未见改善，反而劳动法规日益僵化、两岸关系陷入紧张、对外关系更加孤立。该团体质疑，台当局面对每年的建言，“到底听进去多少，又真正改善了几多”？\
围绕当局两岸政策，工总认为，由数据来看，当前大陆不仅是台湾第一大出口市场，亦是第一大进口来源及首位对外投资地，建议台湾当局摒弃两岸对抗思维，在“求同存异”的现实基础上，以“合作”取代“对立”，为台湾多数民众谋福创利。\
工总现任理事长、同时也是台塑企业总裁的王文渊指出，过去几年，两岸关系紧张，不仅影响岛内观光、零售、饭店业及农渔蔬果产品的出口，也使得岛内外企业对投资台湾却步，2020年新任台湾领导人出炉后，应审慎思考两岸问题以及中国大陆市场。"""

    
'''
