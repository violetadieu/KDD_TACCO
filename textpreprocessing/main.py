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
import adjacent_overlap
#import similarity
import synonym

if __name__=="__main__":
    #data 가저오기
    data=pd.read_csv("data/일반.csv")
    data=data["text"].to_list()
    res = pd.DataFrame()

    kkma=Kkma()

    for text in data[:10]:
        result=collections.defaultdict()
        #원문
        result['sentence']=text
        #text 전처리
        #문장 나누기
        sentences=textpreprocess.splitText(text)
        #단어 나누기
        words=textpreprocess.splitSen(sentences)

        #lemmazation
        wordsAfterLemma=textpreprocess.lemma(words)

        #similar
        #model=similarity.model()
        #similarity.similar(sentences,model)

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

        # All lemmas
        result['adjacent_sentence_overlap_all_lemmas']=0
        result['adjacent_sentence_overlap_all_lemmas_normed']=0
        result['binary_adjacent_sentence_overlap_all_lemmas']=0
        result['adjacent_two_sentence_overlap_all_lemmas']=0
        result['adjacent_two_sentence_overlap_all_lemmas_normed']=0
        result['binary_adjacent_two_sentence_overlap_all_lemmas']=0

        for idx in range(len(sentences)-1):
            result['adjacent_sentence_overlap_all_lemmas']+=\
                adjacent_overlap.adjacent_sentence_overlap_all_lemmas(sentences[idx],sentences[idx+1],kkma)

            result['adjacent_sentence_overlap_all_lemmas_normed'] += \
                adjacent_overlap.adjacent_sentence_overlap_all_lemmas_normed(sentences[idx], sentences[idx + 1], kkma)

            result['binary_adjacent_sentence_overlap_all_lemmas'] += \
                adjacent_overlap.binary_adjacent_sentence_overlap_all_lemmas(sentences[idx], sentences[idx + 1], kkma)

        for idx in range(len(sentences)-2):
            result['adjacent_two_sentence_overlap_all_lemmas'] += \
                adjacent_overlap.adjacent_two_sentence_overlap_all_lemmas(sentences[idx], sentences[idx + 1],sentences[idx+2], kkma)

            result['adjacent_two_sentence_overlap_all_lemmas_normed'] += \
                adjacent_overlap.adjacent_two_sentence_overlap_all_lemmas_normed(sentences[idx], sentences[idx + 1],sentences[idx+2], kkma)

            result['binary_adjacent_two_sentence_overlap_all_lemmas'] += \
                adjacent_overlap.binary_adjacent_two_sentence_overlap_all_lemmas(sentences[idx], sentences[idx + 1],sentences[idx+2], kkma)

        # content lemmas

        result['adjacent_sentence_overlap_content_lemmas'] = 0
        result['adjacent_sentence_overlap_content_lemmas_normed'] = 0
        result['binary_adjacent_sentence_overlap_content_lemmas'] = 0
        result['adjacent_two_sentence_overlap_content_lemmas'] = 0
        result['adjacent_two_sentence_overlap_content_lemmas_normed'] = 0
        result['binary_adjacent_two_sentence_overlap_content_lemmas'] = 0

        for idx in range(len(sentences) - 1):
            result['adjacent_sentence_overlap_content_lemmas'] += \
                adjacent_overlap.adjacent_sentence_overlap_content_lemmas(sentences[idx], sentences[idx + 1], kkma)

            result['adjacent_sentence_overlap_content_lemmas_normed'] += \
                adjacent_overlap.adjacent_sentence_overlap_content_lemmas_normed(sentences[idx], sentences[idx + 1], kkma)

            result['binary_adjacent_sentence_overlap_content_lemmas'] += \
                adjacent_overlap.binary_adjacent_sentence_overlap_content_lemmas(sentences[idx], sentences[idx + 1], kkma)

        for idx in range(len(sentences) - 2):
            result['adjacent_two_sentence_overlap_content_lemmas'] += \
                adjacent_overlap.adjacent_two_sentence_overlap_content_lemmas(sentences[idx], sentences[idx + 1],
                                                                          sentences[idx + 2], kkma)

            result['adjacent_two_sentence_overlap_content_lemmas_normed'] += \
                adjacent_overlap.adjacent_two_sentence_overlap_content_lemmas_normed(sentences[idx], sentences[idx + 1],
                                                                             sentences[idx + 2], kkma)

            result['binary_adjacent_two_sentence_overlap_content_lemmas'] += \
                adjacent_overlap.binary_adjacent_two_sentence_overlap_content_lemmas(sentences[idx], sentences[idx + 1],
                                                                                 sentences[idx + 2], kkma)

        # function lemmas

        result['adjacent_sentence_overlap_function_lemmas'] = 0
        result['adjacent_sentence_overlap_function_lemmas_normed'] = 0
        result['binary_adjacent_sentence_overlap_function_lemmas'] = 0
        result['adjacent_two_sentence_overlap_function_lemmas'] = 0
        result['adjacent_two_sentence_overlap_function_lemmas_normed'] = 0
        result['binary_adjacent_two_sentence_overlap_function_lemmas'] = 0

        for idx in range(len(sentences) - 1):
            result['adjacent_sentence_overlap_function_lemmas'] += \
                adjacent_overlap.adjacent_sentence_overlap_function_lemmas(sentences[idx], sentences[idx + 1], kkma)

            result['adjacent_sentence_overlap_function_lemmas_normed'] += \
                adjacent_overlap.adjacent_sentence_overlap_function_lemmas_normed(sentences[idx], sentences[idx + 1],
                                                                                 kkma)

            result['binary_adjacent_sentence_overlap_function_lemmas'] += \
                adjacent_overlap.binary_adjacent_sentence_overlap_function_lemmas(sentences[idx], sentences[idx + 1],
                                                                                 kkma)

        for idx in range(len(sentences) - 2):
            result['adjacent_two_sentence_overlap_function_lemmas'] += \
                adjacent_overlap.adjacent_two_sentence_overlap_function_lemmas(sentences[idx], sentences[idx + 1],
                                                                              sentences[idx + 2], kkma)

            result['adjacent_two_sentence_overlap_function_lemmas_normed'] += \
                adjacent_overlap.adjacent_two_sentence_overlap_function_lemmas_normed(sentences[idx], sentences[idx + 1],
                                                                                     sentences[idx + 2], kkma)

            result['binary_adjacent_two_sentence_overlap_function_lemmas'] += \
                adjacent_overlap.binary_adjacent_two_sentence_overlap_function_lemmas(sentences[idx], sentences[idx + 1],
                                                                                     sentences[idx + 2], kkma)

        # noun lemmas
        result['adjacent_sentence_overlap_noun_lemmas'] = 0
        result['adjacent_sentence_overlap_noun_lemmas_normed'] = 0
        result['binary_adjacent_sentence_overlap_noun_lemmas'] = 0
        result['adjacent_two_sentence_overlap_noun_lemmas'] = 0
        result['adjacent_two_sentence_overlap_noun_lemmas_normed'] = 0
        result['binary_adjacent_two_sentence_overlap_noun_lemmas'] = 0

        for idx in range(len(sentences) - 1):
            result['adjacent_sentence_overlap_noun_lemmas'] += \
                adjacent_overlap.adjacent_sentence_overlap_noun_lemmas(sentences[idx], sentences[idx + 1], kkma)

            result['adjacent_sentence_overlap_noun_lemmas_normed'] += \
                adjacent_overlap.adjacent_sentence_overlap_noun_lemmas_normed(sentences[idx], sentences[idx + 1],
                                                                                  kkma)

            result['binary_adjacent_sentence_overlap_noun_lemmas'] += \
                adjacent_overlap.binary_adjacent_sentence_overlap_noun_lemmas(sentences[idx], sentences[idx + 1],
                                                                                  kkma)

        for idx in range(len(sentences) - 2):
            result['adjacent_two_sentence_overlap_noun_lemmas'] += \
                adjacent_overlap.adjacent_two_sentence_overlap_noun_lemmas(sentences[idx], sentences[idx + 1],
                                                                               sentences[idx + 2], kkma)

            result['adjacent_two_sentence_overlap_noun_lemmas_normed'] += \
                adjacent_overlap.adjacent_two_sentence_overlap_noun_lemmas_normed(sentences[idx],
                                                                                      sentences[idx + 1],
                                                                                      sentences[idx + 2], kkma)

            result['binary_adjacent_two_sentence_overlap_noun_lemmas'] += \
                adjacent_overlap.binary_adjacent_two_sentence_overlap_noun_lemmas(sentences[idx],
                                                                                      sentences[idx + 1],
                                                                                      sentences[idx + 2], kkma)

        # verb lemmas

        result['adjacent_sentence_overlap_verb_lemmas'] = 0
        result['adjacent_sentence_overlap_verb_lemmas_normed'] = 0
        result['binary_adjacent_sentence_overlap_verb_lemmas'] = 0
        result['adjacent_two_sentence_overlap_verb_lemmas'] = 0
        result['adjacent_two_sentence_overlap_verb_lemmas_normed'] = 0
        result['binary_adjacent_two_sentence_overlap_verb_lemmas'] = 0

        for idx in range(len(sentences) - 1):
            result['adjacent_sentence_overlap_verb_lemmas'] += \
                adjacent_overlap.adjacent_sentence_overlap_verb_lemmas(sentences[idx], sentences[idx + 1], kkma)

            result['adjacent_sentence_overlap_verb_lemmas_normed'] += \
                adjacent_overlap.adjacent_sentence_overlap_verb_lemmas_normed(sentences[idx], sentences[idx + 1],
                                                                              kkma)

            result['binary_adjacent_sentence_overlap_verb_lemmas'] += \
                adjacent_overlap.binary_adjacent_sentence_overlap_verb_lemmas(sentences[idx], sentences[idx + 1],
                                                                              kkma)

        for idx in range(len(sentences) - 2):
            result['adjacent_two_sentence_overlap_verb_lemmas'] += \
                adjacent_overlap.adjacent_two_sentence_overlap_verb_lemmas(sentences[idx], sentences[idx + 1],
                                                                           sentences[idx + 2], kkma)

            result['adjacent_two_sentence_overlap_verb_lemmas_normed'] += \
                adjacent_overlap.adjacent_two_sentence_overlap_verb_lemmas_normed(sentences[idx],
                                                                                  sentences[idx + 1],
                                                                                  sentences[idx + 2], kkma)

            result['binary_adjacent_two_sentence_overlap_verb_lemmas'] += \
                adjacent_overlap.binary_adjacent_two_sentence_overlap_verb_lemmas(sentences[idx],
                                                                                  sentences[idx + 1],
                                                                                  sentences[idx + 2], kkma)

        # adjective lemmas

        result['adjacent_sentence_overlap_adjective_lemmas'] = 0
        result['adjacent_sentence_overlap_adjective_lemmas_normed'] = 0
        result['binary_adjacent_sentence_overlap_adjective_lemmas'] = 0
        result['adjacent_two_sentence_overlap_adjective_lemmas'] = 0
        result['adjacent_two_sentence_overlap_adjective_lemmas_normed'] = 0
        result['binary_adjacent_two_sentence_overlap_adjective_lemmas'] = 0

        for idx in range(len(sentences) - 1):
            result['adjacent_sentence_overlap_adjective_lemmas'] += \
                adjacent_overlap.adjacent_sentence_overlap_adjective_lemmas(sentences[idx], sentences[idx + 1], kkma)

            result['adjacent_sentence_overlap_adjective_lemmas_normed'] += \
                adjacent_overlap.adjacent_sentence_overlap_adjective_lemmas_normed(sentences[idx], sentences[idx + 1],
                                                                              kkma)

            result['binary_adjacent_sentence_overlap_adjective_lemmas'] += \
                adjacent_overlap.binary_adjacent_sentence_overlap_adjective_lemmas(sentences[idx], sentences[idx + 1],
                                                                              kkma)

        for idx in range(len(sentences) - 2):
            result['adjacent_two_sentence_overlap_adjective_lemmas'] += \
                adjacent_overlap.adjacent_two_sentence_overlap_adjective_lemmas(sentences[idx], sentences[idx + 1],
                                                                           sentences[idx + 2], kkma)

            result['adjacent_two_sentence_overlap_adjective_lemmas_normed'] += \
                adjacent_overlap.adjacent_two_sentence_overlap_adjective_lemmas_normed(sentences[idx],
                                                                                  sentences[idx + 1],
                                                                                  sentences[idx + 2], kkma)

            result['binary_adjacent_two_sentence_overlap_adjective_lemmas'] += \
                adjacent_overlap.binary_adjacent_two_sentence_overlap_adjective_lemmas(sentences[idx],
                                                                                  sentences[idx + 1],
                                                                                  sentences[idx + 2], kkma)

        # adverb lemmas
        result['adjacent_sentence_overlap_adverb_lemmas'] = 0
        result['adjacent_sentence_overlap_adverb_lemmas_normed'] = 0
        result['binary_adjacent_sentence_overlap_adverb_lemmas'] = 0
        result['adjacent_two_sentence_overlap_adverb_lemmas'] = 0
        result['adjacent_two_sentence_overlap_adverb_lemmas_normed'] = 0
        result['binary_adjacent_two_sentence_overlap_adverb_lemmas'] = 0

        for idx in range(len(sentences) - 1):
            result['adjacent_sentence_overlap_adverb_lemmas'] += \
                adjacent_overlap.adjacent_sentence_overlap_adverb_lemmas(sentences[idx], sentences[idx + 1], kkma)

            result['adjacent_sentence_overlap_adverb_lemmas_normed'] += \
                adjacent_overlap.adjacent_sentence_overlap_adverb_lemmas_normed(sentences[idx], sentences[idx + 1],
                                                                                   kkma)

            result['binary_adjacent_sentence_overlap_adverb_lemmas'] += \
                adjacent_overlap.binary_adjacent_sentence_overlap_adverb_lemmas(sentences[idx], sentences[idx + 1],
                                                                                   kkma)

        for idx in range(len(sentences) - 2):
            result['adjacent_two_sentence_overlap_adverb_lemmas'] += \
                adjacent_overlap.adjacent_two_sentence_overlap_adverb_lemmas(sentences[idx], sentences[idx + 1],
                                                                                sentences[idx + 2], kkma)

            result['adjacent_two_sentence_overlap_adverb_lemmas_normed'] += \
                adjacent_overlap.adjacent_two_sentence_overlap_adverb_lemmas_normed(sentences[idx],
                                                                                       sentences[idx + 1],
                                                                                       sentences[idx + 2], kkma)

            result['binary_adjacent_two_sentence_overlap_adverb_lemmas'] += \
                adjacent_overlap.binary_adjacent_two_sentence_overlap_adverb_lemmas(sentences[idx],
                                                                                       sentences[idx + 1],
                                                                                       sentences[idx + 2], kkma)


        iter=pd.DataFrame([result])
        res=res.append(iter)
    res.to_csv("result.csv",encoding="utf-8-sig")

    print("end")
        #connectives

        #기타(LSA, LDA, word2vec)
