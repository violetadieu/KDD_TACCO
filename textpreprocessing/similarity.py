import torch
import json
import pandas as pd
import numpy as np
from torch.utils.data import DataLoader
from datasets import load_dataset
from sentence_transformers import SentenceTransformer,  LoggingHandler, losses, models, util
from sentence_transformers.evaluation import EmbeddingSimilarityEvaluator
from sentence_transformers.readers import InputExample
from transformers import AutoModel, AutoTokenizer

modelName="klue/bert-base"
tokenizerName="klue/bert-base"
embeddingModelName=models.Transformer(modelName)
tokenizer = AutoTokenizer.from_pretrained(tokenizerName)


def readTrainData(path):
    trainDataset = []
    with open(path, 'rb') as file:
        STSdata = json.load(file)

    for item in STSdata:
        score = float(item['labels']['label']) / 5.0

        inputEx = InputExample(
            texts=[item["sentence1"], item["sentence2"]],
            label=score
        )
        trainDataset.append(inputEx)

    return trainDataset

def model():
    BATCH_SIZE=32
    EPOCH=4
    outputPath=(modelName+"_epoch-"+str(EPOCH)).replace("/","-")
    outputPath='./outputs/'+outputPath

    pooler = models.Pooling(
        embeddingModelName.get_word_embedding_dimension(),
        pooling_mode_mean_tokens=True,
        pooling_mode_cls_token=False,
        pooling_mode_max_tokens=False,
    )

    model = SentenceTransformer(modules=[embeddingModelName, pooler])

    dataName="./dataset/klue-sts-v1.1_train.json"
    trainDataset=readTrainData(dataName)

    trainDataLoader=DataLoader(
    trainDataset,
    shuffle=True,
    batch_size=BATCH_SIZE
    )
    trainLoss=losses.CosineSimilarityLoss(model=model)

    evaluator=EmbeddingSimilarityEvaluator.from_input_examples(
    trainDataset,
    name="sts-vali"
    )

    model.fit(
    train_objectives=[(trainDataLoader, trainLoss)],
        evaluator=evaluator,
        epochs=EPOCH,
        evaluation_steps=1000,
        output_path=outputPath
     )

    return model

def similar(docs,model):

    document_embeddings = model.encode(docs)

    query = docs[0]
    query_embedding = model.encode(query)

    top_k = min(5, len(docs))

    # 입력 문장 - 문장 후보군 간 코사인 유사도 계산 후,
    cos_scores = util.pytorch_cos_sim(query_embedding, document_embeddings)[0]

    # 코사인 유사도 순으로 `top_k` 개 문장 추출
    top_results = torch.topk(cos_scores, k=top_k)

    print(f"입력 문장: {query}")
    print(f"\n<입력 문장과 유사한 {top_k} 개의 문장>\n")

    for i, (score, idx) in enumerate(zip(top_results[0], top_results[1])):
        print(f"{i+1}: {docs[idx]} {'(유사도: {:.4f})'.format(score)}\n")