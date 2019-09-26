# -*- coding: utf-8 -*-
"""
Created on Thu Sep 26 00:23:47 2019

@author: K
"""

import fasttext
model=fasttext.train_unsupervised(input="project.train", lr=0.1, epoch=20, wordNgrams=2,dim=150)
model.save_model("fast2.bin")


