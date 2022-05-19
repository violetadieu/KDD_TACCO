import sys, os
import re
import numpy as np
import pandas as pd
import collections
import time

import konlpy

import textpreprocess
import TTR


if __name__=="__main__":
    #data 가저오기
    data=pd.read_csv("data/train.csv")
    data=data["text"].to_list()
    data.sort(key=len)

    for text in data:
        result=collections.defaultdict()

        #text 전처리
        #문장 나누기
        sentences=textpreprocess.splitText(text)
        #단어 나누기
        words=textpreprocess.splitSen(sentences)

        #lemmazation
        wordsAfterLemma=textpreprocess.lemma(words)

        #TTR
            #lemmattr
        result['lemmattr']=TTR.lemmaTtr(wordsAfterLemma)
            #lemma_mattr
        result['lemmaMattr']=TTR.lemmaMattr(wordsAfterLemma)
            #lexical_density_tokens
        result['lexicalDensityTokens']=TTR.lexicalDensityTokens(wordsAfterLemma)
            #lexical_density_tokens
        result['lexicalDensityTypes'] = TTR.lexicalDensityTypes(wordsAfterLemma)
            #contenTtr
        result['contentTtr']=TTR.contentTtr(wordsAfterLemma)
        #overlap

        #pronoun

        #connectives

        #기타(LSA, LDA, word2vec)
