# -*- coding: utf-8 -*-
"""
Created on Wed Aug 14 15:24:45 2019

@author: K
"""

from gensim.models import Word2Vec  
from pyplt_my import HIT 
from collections import defaultdict
model = Word2Vec.load("word2vec.model") 
#similar=get_related_words(['说','指出','报道','提出','表示','称'], model)   # 找说的近义词 
#ok#sentence="国务院总理李克强调研上海外高桥提出，支持上海积极探索新机制。" 
#sentence="围绕当局两岸政策，工总认为，由数据来看，当前大陆不仅是台湾第一大出口市场，亦是第一大进口来源及首位对外投资地，建议台湾当局摒弃两岸对抗思维，在“求同存异”的现实基础上，以“合作”取代“对立”，为台湾多数民众谋福创利。"
#sentence="台湾工业总会指出，2015年的白皮书就特别提到台湾面临“五缺”（缺水、缺电、缺工、缺地、缺人才）困境，使台湾整体投资环境走向崩坏。然而四年过去，“五缺”未见改善，反而劳动法规日益僵化、两岸关系陷入紧张、对外关系更加孤立。该团体质疑，台当局面对每年的建言，“到底听进去多少，又真正改善了几多”？"
#oksentence="国务院关税税则委员会有关负责人表示，美方此举严重违背中美两国元首阿根廷会晤共识和大阪会晤共识，背离了磋商解决分歧的正确轨道。中方将不得不采取必要的反制措施。"
#ok#sentence="据日本共同社刚刚报道，日本首相安倍晋三今天上午以自民党总裁名义向靖国神社供奉“玉串料”(祭祀费)。安倍本人并未露面，祭祀费由自民党总裁特别助理稻田朋美代为献上。"
#ok#sentence="8月15日，中国联通举办年中业绩发布会，中国联通董事长王晓初表示，目前联通推出的5G功能费用最低为190元，未来将根据用户的质量、速度的不同差异化定价。"
#ok3sentence="根据近期媒体报道，中国电信的5G套餐资费也已经基本确定，价位段将从199元到599元不等。"
#ok#sentence="中国联通表示，得益于良好的支出管控，自由现金流保持强劲，达到人民币215亿元，公司财务实力持续增强，财务状况更加稳健。"
#sentence="中国联通称，上半年，创新业务成为稳定中国联通收入的主要驱动力。产业互联网业务收入同比增长43%"
#sentence="展望未来，中国联通称将按技术进展、市场和业务需求、行业竞争态势等动态精准投入5G建设，推进5G生态建设。"
#sentence="回首过去，他指出由数据来看，当前大陆不仅是台湾第一大出口市场，亦是第一大进口来源及首位对外投资地"
#sentence="工总现任理事长、同时也是台塑企业总裁的王文渊指出，过去几年，两岸关系紧张，不仅影响岛内观光、零售、饭店业及农渔蔬果产品的出口，也使得岛内外企业对投资台湾却步，2020年新任台湾领导人出炉后，应审慎思考两岸问题以及中国大陆市场"
#sentence="台湾工业总会是岛内最具影响力的工商团体之一，2008年以来，该团体连续12年发表对台当局政策的建言白皮书，集中反映岛内产业界的呼声。"
#sentence="瑞银大中华区消费品行业研究主管彭燕燕表示，近期对中国一线到五线城市的3000名消费者调查显示，相比2018年，消费者信心有所提高，消费者对其收入增长、财富增值和财务保障的信心均强于去年的调查结果。"
#sentence="线上、线下能够较好融合的品牌或者零售商，在未来的竞争格局中会越做越大，获取更多市场份额。”彭燕燕说。"
#sentence="“我们通过大量的市场研究来探索年轻人喜欢的潮款，比如和葫芦兄弟的一款联名鞋，上市后销量表现就很不错。”上海回力鞋业有限公司副总经理张玉明说，公司还积极拥抱互联网，目前线上销量约占总销量的70%。"

sentence="贝恩公司全球合伙人邓旻表示，随着中国消费者日益成熟，他们可以利用的渠道变得越来越先进。对于企业而言，需了解并融合新的零售模式，同时专注于以消费者为中心，为消费者提供更多、更好的产品。"


ltp=HIT(sentence)    
sents=ltp.sentence_splitter()  
result=[]

ltp2=HIT(sentence)
words=ltp2.segmentor()
ltp2.posttagger()
NER=ltp2.ner() 
parse=ltp2.parse()[1]  # 依存分析结果

# 找head
for i in range(len(parse)):
    if parse[i][1]=='HED':
        head=i 
       
head_word=words[head]
print("the origin head is ",head_word)


if head!=0:  # eg：head=0"展望未来 (以动词开头的)
    if similar[head_word]>=1: 
        sub_index,sub_word= get_sub_words(head, parse) 
        result.append( sub_word) 
        result.append( head_word)
        if words[head+1]=='，':

            result.append(''.join(words[head+2:])) 
        else:
            result.append(''.join(words[head+1:]))  
        #print(result)
 
new_head,new_head_word=VOB(head, parse)  #工总现任理事长、同时也是。。。(eg,真正的核心和head是VOB)
if  new_head_word!=0:
    if similar[new_head_word]>=1:
        sub_index,sub_word= get_sub_words(new_head, parse) 
        result.append( sub_word) 
        result.append( new_head_word)
        if words[new_head+1]=='，':
        
            result.append(''.join(words[ new_head+2:])) 
        else:
            result.append(''.join(words[ new_head+1:]))  
    
re=get_head_parral_words(head, parse)   #8月15日，中国联通举办年中业绩发布会 。。。 这种情况(eg,真正的核心和head是COO)
if len(re)>0:
    for (parra_index,parral_word) in re:
        if   parral_word!=0:
            if similar[parral_word]>=1:
                sub_index,sub_word= get_sub_words( parra_index, parse) 
                result.append( sub_word) 
                result.append(parral_word)
                if words[ parra_index+1]=='，':
                    result.append(''.join(words[ parra_index+2:])) 
                else:
                    result.append(''.join(words[ parra_index+1:]))  

new_head,new_head_word=get_genju(parse)   #根据近期媒体报道，中国电信的5G...（e.g ：根据。。什么报道，类型）
if  new_head_word!=0:
    if similar[new_head_word]>=1:
        sub_index,sub_word= get_sub_words(new_head, parse) 
        result.append( sub_word) 
        result.append( new_head_word)
        if words[new_head+1]=='，':
          
            result.append(''.join(words[ new_head+2:])) 
        else:
            result.append(''.join(words[ new_head+1:]))  
  
print(result)


def  get_head_parral_words(head, parse):
    re=[]
    for i in range(len(parse)):
      
        if parse[i][0]==head+1 and parse[i][1]=='COO':
            print("the parral head:is ",words[i] )
            re.append((i,words[i]))
    return re 
   
   #return -1,0
def get_genju(parse):  #根据。。报道 
     if parse[0][1]=='ADV':
         for i in range(len(parse)):
            if parse[i][0]==1 and parse[i][1]=='POB':#and ('Ni'in NER[i] or 'Nh'in NER[i]):
                print('根据_head:',words[i] ) 
                return i,words[i] 
     return -1,0
def  VOB(head, parse):  
    for i in range(len(parse)):
        if parse[i][0]==head+1 and parse[i][1]=='VOB':
            print("the VOB head:is ",words[i] )
            return i,words[i] 
    return -1,0

    
def  get_sub_words(head, parse):
    for i in range(len(parse)):
        if parse[i][0]==head+1 and parse[i][1]=='SBV':#and ('Ni'in NER[i] or 'Nh'in NER[i]):
            sub=i 
            print("主语是: ",words[i])
            return i,words[i]
    


#搜索代码
def get_related_words(initial_words, model):
    """
    @initial_words are initial words we already know
    @model is the word2vec model
    """
    
    unseen = initial_words
    
    seen = defaultdict(int)
    
    max_size = 1000  # could be greater
    
    while unseen and len(seen) < max_size:
        if len(seen) % 50 == 0: 
            print('seen length : {}'.format(len(seen)))
            
        node = unseen.pop(0)
        
        new_expanding = [w for w, s in model.most_similar(node, topn=20)]
        
        unseen += new_expanding
        
        seen[node] += 1
        
        # optimal: 1. score function could be revised
        # optimal: 2. using dymanic programming to reduce computing time
    
    return seen

