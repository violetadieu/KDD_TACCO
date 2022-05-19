import collections

from konlpy.tag import Kkma

#단어 전체 ttr
def lemmaTtr(words):

    types=collections.defaultdict(int)
    for word in words:
        types[word]=types[word]+1

    return len(types)/len(words)

#단어 50개단위 TTR
def lemmaMattr(words):
    if len(words)<50:
        return -1
    idx=0
    ttr=0.0
    cnt=0
    while idx<=len(words):
        types=collections.defaultdict(int)
        ttrList=words[idx:idx+50]
        for word in ttrList:
            types[word]=types[word]+1
        cnt+=1
        ttr+=len(types)/len(ttrList)
        idx+=50

    return ttr/cnt

#어휘형태소(명사 동사 형용사 부사) 개수의 비율
def lexicalDensityTokens(words):

    kkma=Kkma()

    cnt=0
    totalCnt=0

    for word in words:
        pos=kkma.pos(word)
        for morp in pos:
            totalCnt+=len(pos)
            if "NN" in morp[1] or "V" in morp[1] or "MA" in morp[1]:
                cnt+=1

    return cnt/totalCnt

#어휘형태소 종류의 비율
def lexicalDensityTypes(words):

    kkma = Kkma()

    type=collections.defaultdict(int)
    totalCnt=0

    for word in words:
        pos = kkma.pos(word)
        for morp in pos:
            totalCnt+=len(pos)
            if "NN" in morp[1] or "V" in morp[1] or "MA" in morp[1]:
                type[morp[0]]=type[morp[0]]+1

    return len(type) / totalCnt

def contentTtr(words):

    return 0

def functionTtr():
    return 0

def functionMattr():
    return 0

def nounTtr():
    return 0

def verbTtr():
    return 0

def adjTtr():
    return 0

def advTtr():
    return 0

def prpTtr():
    return 0

def argumentTtr():
    return 0

def bigramLemmaTtr():
    return 0

def trigramLemmaTtr():
    return 0
