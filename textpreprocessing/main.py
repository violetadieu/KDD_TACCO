import pandas as pd
import collections

from konlpy.tag import Kkma

import textpreprocess
import TTR
import adjacent_overlap
import similarity
import topic
# 대명사 목록, 지시대명사 -> 인칭대명사 순서
pronounList = ['이', '그', '저', '이것', '그것', '저것', '무엇', '여기', '저기', '거기', '어디',
               '저희', '본인', '그대', '귀하', '너희', '당신', '여러분', '임자', '자기', '자네', '이런',
               '그들', '그녀', '당신', '저희', '놈', '얘', '걔', '쟤', '누구']

class tmp_k():
    leng=0
    data=list()
    result=list()
    def pos(self,word):
        for item in self.data:
            if word in item:
                result=item.split("/")
                return result

def conjuctions(kkma, wordsAfterLemma):
    type = collections.defaultdict(int)
    totalCnt = 0

    for word in words:
        morp = kkma.pos(word)
        #for morp in pos:
        if morp[1] == "MAG":
            type[morp[0]] = type[morp[0]] + 1
            totalCnt += 1
    if totalCnt == 0:
        return 0
    return len(type) / totalCnt


if __name__ == "__main__":
    # data 가저오기
    data = pd.read_csv("data/GT.csv")
    data = data["text"].to_list()
    res = pd.DataFrame()

    kkma = tmp_k()
    kkma.data=data
    kkma.leng=len(data)

    for text in range(0,1):
        text="독도 주변 바다에는 분지 모양의 지형이 존재하는데, 이곳은 육지에서 멀리 떨어져 있어 하천을 거쳐 들어오는 퇴적물의 공급이 잘 이루어지지 않으며 수심이 깊어 온도가 낮다. 지질적 특성의 영향을 많이 받는 메탄 하이드레이트는 이와 같은 지형적 특성을 나타내는 곳에 주로 분포한다."



        result = collections.defaultdict()
        # 원문
        result['sentence'] = text
        # text 전처리
        # 문장 나누기
        try:
            sentences = textpreprocess.splitText(text)
        except:
            continue
        # 단어 나누기
        #words = textpreprocess.splitSen(sentences)
        words=list()
        for item in data:
            words.append(item.split("/")[0])

        # lemmazation
        wordsAfterLemma = words#textpreprocess.lemma(words)
        result['lemmaCnt'] = len(wordsAfterLemma)

        # similar
        #model = similarity.model()
        #result['average_similarity']=similarity.similar(text, model)

        #topic

        # conjuctions
        result['conjuctions'] = conjuctions(kkma, wordsAfterLemma)

        # TTR
        # lemmattr
        result['lemmattr'] = TTR.lemmaTtr(wordsAfterLemma)
        # lemma_mattr
        result['lemmaMattr'] = TTR.lemmaMattr(wordsAfterLemma)
        # lexical_density_tokens
        result['lexicalDensityTokens'] = TTR.lexicalDensityTokens(wordsAfterLemma, kkma)
        # lexical_density_tokens
        result['lexicalDensityTypes'] = TTR.lexicalDensityTypes(wordsAfterLemma, kkma)
        # contentTtr
        result['contentTtr'] = TTR.contentTtr(wordsAfterLemma, kkma)
        # functionTtr
        result['functionTtr'] = TTR.functionTtr(wordsAfterLemma, kkma)
        # functionMattr
        # result['functionMattr']=TTR.functionMattr(wordsAfterLemma,kkma)
        # nounTtr
        # uniqueNoun,nounNum
        result['nounTtr'] = TTR.nounTtr(wordsAfterLemma, kkma)
        # verbTtr
        result['verbTtr'] = TTR.verbTtr(wordsAfterLemma, kkma)
        # adjTtr
        result['adjTtr'] = TTR.adjTtr(wordsAfterLemma, kkma)
        # advTtr
        result['advTtr'] = TTR.advTtr(wordsAfterLemma, kkma)
        # prpTtr
        # uniquePronoun,pronounNum, result['prpTtr'] = TTR.prpTtr(wordsAfterLemma, kkma,pronounList)
        # argumentTtr 대명사는 나중에~
        # result['argumentTtr'] = TTR.argumentTtr(wordsAfterLemma, kkma,uniquePronoun)
        # advTtr
        result['bigramLemmaTtr'] = TTR.bigramLemmaTtr(wordsAfterLemma)
        # advTtr
        result['trigramLemmaTtr'] = TTR.trigramLemmaTtr(wordsAfterLemma)

        # All lemmas
        result['adjacent_sentence_overlap_all_lemmas'] = 0
        result['adjacent_sentence_overlap_all_lemmas_normed'] = 0
        result['binary_adjacent_sentence_overlap_all_lemmas'] = 0
        result['adjacent_two_sentence_overlap_all_lemmas'] = 0
        result['adjacent_two_sentence_overlap_all_lemmas_normed'] = 0
        result['binary_adjacent_two_sentence_overlap_all_lemmas'] = 0

        for idx in range(len(sentences) - 1):
            result['adjacent_sentence_overlap_all_lemmas'] += \
                adjacent_overlap.adjacent_sentence_overlap_all_lemmas(sentences[idx], sentences[idx + 1], kkma)

            result['adjacent_sentence_overlap_all_lemmas_normed'] += \
                adjacent_overlap.adjacent_sentence_overlap_all_lemmas_normed(sentences[idx], sentences[idx + 1], kkma)

            result['binary_adjacent_sentence_overlap_all_lemmas'] += \
                adjacent_overlap.binary_adjacent_sentence_overlap_all_lemmas(sentences[idx], sentences[idx + 1], kkma)

        for idx in range(len(sentences) - 2):
            result['adjacent_two_sentence_overlap_all_lemmas'] += \
                adjacent_overlap.adjacent_two_sentence_overlap_all_lemmas(sentences[idx], sentences[idx + 1],
                                                                          sentences[idx + 2], kkma)

            result['adjacent_two_sentence_overlap_all_lemmas_normed'] += \
                adjacent_overlap.adjacent_two_sentence_overlap_all_lemmas_normed(sentences[idx], sentences[idx + 1],
                                                                                 sentences[idx + 2], kkma)

            result['binary_adjacent_two_sentence_overlap_all_lemmas'] += \
                adjacent_overlap.binary_adjacent_two_sentence_overlap_all_lemmas(sentences[idx], sentences[idx + 1],
                                                                                 sentences[idx + 2], kkma)

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
                adjacent_overlap.adjacent_sentence_overlap_content_lemmas_normed(sentences[idx], sentences[idx + 1],
                                                                                 kkma)

            result['binary_adjacent_sentence_overlap_content_lemmas'] += \
                adjacent_overlap.binary_adjacent_sentence_overlap_content_lemmas(sentences[idx], sentences[idx + 1],
                                                                                 kkma)

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
                adjacent_overlap.adjacent_two_sentence_overlap_function_lemmas_normed(sentences[idx],
                                                                                      sentences[idx + 1],
                                                                                      sentences[idx + 2], kkma)

            result['binary_adjacent_two_sentence_overlap_function_lemmas'] += \
                adjacent_overlap.binary_adjacent_two_sentence_overlap_function_lemmas(sentences[idx],
                                                                                      sentences[idx + 1],
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

        iter = pd.DataFrame([result])
        res = res.append(iter)
    res.to_csv("고등_result.csv", encoding="utf-8-sig")

    print("end")
    # connectives

    # 기타(LSA, LDA, word2vec)
