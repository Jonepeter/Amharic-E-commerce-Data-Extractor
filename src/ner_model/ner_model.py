import pandas as pd
from datasets import load_dataset, Dataset, DatasetDict, ClassLabel, Sequence
from transformers import AutoTokenizer, AutoModelForTokenClassification, TrainingArguments, Trainer, DataCollatorForTokenClassification
import numpy as np
from seqeval.metrics import classification_report

def read_conll(filepath):
    sentences, labels = [], []
    with open(filepath, encoding='utf-8') as f:
        words, tags = [], []
        for line in f:
            if line.strip() == "":
                if words:
                    sentences.append(words)
                    labels.append(tags)
                    words, tags = [], []
            else:
                splits = line.strip().split()
                words.append(splits[0])
                tags.append(splits[-1])
        if words:
            sentences.append(words)
            labels.append(tags)
    data = {'tokens': sentences, 'ner_tags': labels}
    dataset = pd.DataFrame(data)
    return dataset, sentences,labels

def tokenize_and_align_labels(examples):
    model_checkpoint = "xlm-roberta-base"  # or "Davlan/bert-tiny-amharic" or "Davlan/afro-xlmr-base"
    tokenizer = AutoTokenizer.from_pretrained(model_checkpoint)
    unique_tags = set(tag for doc in examples['labels'] for tag in doc)
    label_list = sorted(list(unique_tags))
    label2id = {l: i for i, l in enumerate(label_list)}
    id2label = {i: l for l, i in label2id.items()}
    tokenized_inputs = tokenizer(examples["tokens"], truncation=True, is_split_into_words=True)
    labels = []
    for i, label in enumerate(examples["ner_tags"]):
        word_ids = tokenized_inputs.word_ids(batch_index=i)
        label_ids = []
        previous_word_idx = None
        for word_idx in word_ids:
            if word_idx is None:
                label_ids.append(-100)
            elif word_idx != previous_word_idx:
                label_ids.append(label2id[label[word_idx]])
            else:
                label_ids.append(-100)
            previous_word_idx = word_idx
        labels.append(label_ids)
    tokenized_inputs["labels"] = labels
    return tokenized_inputs