import sys, os
import re
import numpy as np
import pandas as pd
import collections
import time

import konlpy
from konlpy.tag import Kkma

import textpreprocess
import TTR


if __name__=="__main__":
    #data 가저오기
    data=pd.read_csv("data/train.csv")
    data=data["text"].to_list()
    data.sort(key=len)

    kkma=Kkma()

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
        result['lexicalDensityTokens']=TTR.lexicalDensityTokens(wordsAfterLemma,kkma)
            #lexical_density_tokens
        result['lexicalDensityTypes'] = TTR.lexicalDensityTypes(wordsAfterLemma,kkma)
            #contentTtr
        result['contentTtr']=TTR.contentTtr(wordsAfterLemma,kkma)
            #functionTtr
        result['functionTtr']=TTR.functionTtr(wordsAfterLemma,kkma)
            #functionMattr
        result['functionMattr']=TTR.functionMattr(wordsAfterLemma,kkma)
            #nounTtr
        result['nounTtr']=TTR.nounTtr(wordsAfterLemma,kkma)
            #verbTtr
        result['verbTtr'] = TTR.verbTtr(wordsAfterLemma, kkma)
            #adjTtr
        result['adjTtr'] = TTR.adjTtr(wordsAfterLemma, kkma)
            #advTtr
        result['advTtr'] = TTR.advTtr(wordsAfterLemma, kkma)
            #prpTtr 대명사는 나중에~
        result['prpTtr'] = TTR.prpTtr(wordsAfterLemma, kkma)
            #argumentTtr 대명사는 나중에~
        result['argumentTtr'] = TTR.argumentTtr(wordsAfterLemma, kkma)
            #advTtr
        result['bigramLemmaTtr'] = TTR.bigramLemmaTtr(wordsAfterLemma)
            #advTtr
        result['trigramLemmaTtr'] = TTR.trigramLemmaTtr(wordsAfterLemma)


        #connectives

        #기타(LSA, LDA, word2vec)
