# -*- coding: utf-8 -*-
'''
Created on Wed Sep 25 21:48:36 2019

@author: K
'''

import joblib
import fasttext
import pyplt_test #之前哈工大的包
import re
import numpy as np 
from sklearn.decomposition import PCA
from sklearn.metrics.pairwise import cosine_similarity 
import numpy as np
model = fasttext.load_model("fast2.bin")  # 导入fst模型； 

embedding_size = 150


threshold='0.6' #相似度大小阈值



class Word:  #每个单词
    def __init__(self, text, vector):
        self.text = text
        self.vector = vector


class Sentence:  # 每个句子
    def __init__(self, word_list):
        self.word_list = word_list

    def len(self) -> int:
        return len(self.word_list)

def token3(string):   #文本预处理，正则化
    string2=string.replace('\\n','') 
    #print(string2)
    temp=re.findall('\w+', string2)
    final= "".join(temp)
    return final 


def get_word_frequency(word_text, looktable):  # 计算语料库中每个单词出现的频率
    if word_text in looktable:
        return looktable[word_text]
    else:
        return 1.0



def sentence_to_vec(sentence_list, embedding_size, looktable, a=1e-3): #核心算法：参照2017 普林斯顿A S IMPLE BUT T OUGH - TO -B EAT B ASELINE FOR S EN -TENCE E MBEDDINGS
    sentence_set = []
    for sentence in sentence_list:
        vs = np.zeros(embedding_size)  # add all word2vec values into one vector for the sentence
        sentence_length = sentence.len()
        for word in sentence.word_list:
            
            a_value = a / (a + get_word_frequency(word.text, looktable))  # smooth inverse frequency, SIF
           
            
            vs = np.add(vs, np.multiply(a_value, word.vector))  # vs += sif * word_vector

        vs = np.divide(vs, sentence_length)  # weighted average
        sentence_set.append(vs)  # add to our existing re-calculated set of sentences

    # calculate PCA of this sentence set
    pca = PCA()#(n_components=embedding_size)
    pca.fit(np.array(sentence_set))
    u = pca.components_[0]  # the PCA vector
    u = np.multiply(u, np.transpose(u))  # u x uT

    # pad the vector?  (occurs if we have less sentences than embeddings_size)
    if len(u) < embedding_size:
        for i in range(embedding_size - len(u)):
            u = np.append(u, 0)  # add needed extension for multiplication below

    # resulting sentence vectors, vs = vs -u x uT x vs
    sentence_vecs = []
    for vs in sentence_set:
        sub = np.multiply(u, vs)
        sentence_vecs.append(np.subtract(vs, sub))

    return sentence_vecs



def final_model(paragraph): # 计算每个句子与整篇文档的相似度，大于阈值的留下 
    
    ltp = pyplt_test.HIT(paragraph) 
    sents=ltp.sentence_splitter() 
    sents=[s for s in sents if len(s)>0]
    
    id_sent={}  # 构建字典，方便后面还原句子
    for i ,s in enumerate(sents):
        id_sent[i]=s
        
        
    
    
    sents_clean=[token3(s) for s in sents]
    
   # print(len(sents_clean))
    
    
    assert len(sents_clean)==len(sents)
        
    s = [] 
    allsent=[]
    whole_words=[] 
    for sent in sents_clean:
        s = []
        ltp2=pyplt_test.HIT(sent)
        words=ltp2.segmentor()
        for word in words:
            vec = model.get_word_vector(word)
            s.append(Word(word, vec))
            whole_words.append(Word(word, vec))
    
        ss1 = Sentence(s)
    
        allsent.append(ss1) 
    whole_sents=Sentence(whole_words ) # 整篇文档 
    allsent.append(whole_sents)
    
   # print(len(allsent))
    
    sentence_vectors = sentence_to_vec(allsent, embedding_size, looktable=word_list)
    len_sentences = len(sentence_vectors)
    
    
    #print(len_sentences)
    assert len_sentences==len(sents)+1
    paragragh_vec=sentence_vectors[-1] #文档向量
    
    
    vital_index=[]
    
    for i in range(len_sentences-1):
        
            sim = cosine_similarity([sentence_vectors[i],paragragh_vec])
            sim_value=sim [0][1]
            
            if  sim_value>float(threshold) :
                
                vital_index.append(i)
                
    #print(vital_index)            
    final_result=""            
    for index in  vital_index: # 在字典取出相似度大的句子，留下
        final_result+=id_sent[index]
         
    print ( final_result)           
            
    
    
      
if __name__ == '__main__':    
    

    word_list=joblib.load('word_count_list.pkl')
    #print('完成词频字典载入')
    
    #paragraph="""上海市公安机关迅速查明曾伯克父青铜组器的拍卖委托人和实际持有人周某（上海居民）有重大犯罪嫌疑，并于3月8日正式立案侦查。在外交努力与刑事侦查合力推动下，日本拍卖机构公开声明中止文物拍卖。此后，经过文物部门和公安机关多方施加压力，文物持有人于2019年7月同意将该组青铜器上缴国家并配合公安机关调查。曾伯克父青铜组器实物鉴定与接收工作完成后，国家文物局在中国驻日本使馆全力支持下，以最快速度完成文物日本出境手续，8月23日携运文物星夜抵京，8月24日凌晨安全入库。文物持有人周某于8月23日随公安机关工作组一同回国配合调查。"""
    
    '''
    paragraph="""《我和我的祖国》定档9月30日上午9时在内地影院上映，从预售的结果可以看出，电影《我和我的祖国》可谓一骑绝尘，作为献礼70周年的影片《我和我的祖国》为何如此受欢迎呢？

首先这部影片是由陈凯歌、张一白、管虎、薛晓路、徐峥、宁浩、文牧野七位华语顶级导演联合指导，集合了黄渤、欧豪、张译、吴京、杜江、朱一龙、惠英红、葛优、任达华、宋佳、刘昊然等众位华语影坛有口皆碑的实力派演员出演，如此强大的阵容实属罕见。

剧照一推出时就吸引了观众的眼球，这部中国电影界史无前例的大制作，光看制作团队与演员阵容就让人非常震撼。"""
   
   
    paragraph="""早晨，我还是像往常那样起床。慢慢地拉开了窗帘，啊！呈现在我眼前的是一片洁白。快看，那是雪呀！我一时兴奋，顿时睡意全消。快步跑向窗台，只见雪花纷纷扬扬地飘落到地上，像是一只只翩翩起舞的白蝴蝶；又好似隆冬的使者在空中荡着秋千。不一会儿，大地变得一片银白，好似铺上了厚厚的白地毯。
中午，雪停了，太阳高照。孩子们在雪中尽情地玩耍，有的玩堆雪人，有的玩打雪仗，还有的玩“切蛋糕”。其中，最热闹的就是“切蛋糕”了。我、张泽、鲁浩洋还有王子靓做了一个厚为五厘米的大“蛋糕”，我们给它取名为“无敌大蛋糕”。因为它太大了，就找来我们班的同学们分“吃”蛋糕。欢声笑语在雪地里回荡，多麽有趣呀！这就是冬爷爷送给我们这些天真小朋友最好的礼物。
晚上，天黑了，大地被白雪映照得一片雪亮。下班回来的人们看见了前方的路。从远处望去，家家户户灯火辉煌，这又是一番美景，看上去有一种温馨的感觉。
我要大声地赞美冬天：感谢冬爷爷为我们带来四季中最美丽、最快乐的冬季。"""
   '''
   
    paragraph="""中国日报网9月25日电 今天是新中国民航史上一个值得永远铭记的日子。在经历了7次综合模拟演练、3场验证试飞之后，北京大兴国际机场于今天上午正式投运。
“凤凰展翅，翱翔九天”。作为20年内全球范围规划新建设的最大机场之一，大兴国际机场从开工建设到“展翅起飞”，每一步都吸引着全球的目光。
英国路透社25日报道称，在中华人民共和国成立70周年前夕，北京大兴国际机场正式投入运营。这项耗资数百亿美元的浩大工程，在不到5年的时间内就完工了，将进一步促进中国基础设施建设的发展。
报道称，这座机场由已故英籍伊拉克建筑师扎哈 哈迪德(Zaha Hadid)设计，预计旅客吞吐量最终将达到1亿人次，将大幅缓解北京首都国际机场的压力。目前，首都国际机场已达运力极限。
新加坡《海峡时报》网站25日报道称，大兴国际机场距天安门广场直线距离46公里，是首都国际机场与市中心距离的约两倍。不过，配套的高铁、城际快车、地铁和巴士等形成的交通网，将使乘客方便快捷地抵达机场。此外，河北和天津等地区的乘客也可以借助便捷的交通网享受到大兴机场所带来的出行便利。"""

    final_model(paragraph)
    
            
