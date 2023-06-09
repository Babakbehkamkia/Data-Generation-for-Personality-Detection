# -*- coding: utf-8 -*-
"""GPT2_fine_tune.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1tHRDep3IP3NnDESeDgnIkUun171GjuOD
"""

# !pip install transformers

import pandas as pd
import torch
from torch.utils.data import Dataset, random_split
from transformers import GPT2Tokenizer, TrainingArguments, Trainer, GPT2LMHeadModel
import pickle

torch.manual_seed(42)

tokenizer = GPT2Tokenizer.from_pretrained('gpt2-medium', bos_token='<|startoftext|>',
                                          eos_token='<|endoftext|>', pad_token='<|pad|>')
model = GPT2LMHeadModel.from_pretrained('gpt2-medium').cuda()
model.resize_token_embeddings(len(tokenizer))

# from google.colab import drive
# drive.mount('/content/drive')

# path = "/content/drive/My Drive/CS224N/final_phase2/"

data = pd.read_csv("../Datasets/raw/mbti_tweets.csv")
# data

types = [
    "ENFP",
    "ENFJ",
    "ESTJ",
    "ESFJ",
    "ESTP",
    "ESFP",
    "ENTJ",
    "ENTP",
    "INFP",
    "INTP",
    "INFJ",
    "INTJ",
    "ISFP",
    "ISTP",
    "ISFJ",
    "ISTJ"
]

class MBTIDataset(Dataset):
    def __init__(self, txt_list, tokenizer, max_length):
        self.input_ids = []
        self.attn_masks = []
        self.labels = []
        for txt in txt_list:
            encodings_dict = tokenizer('<|startoftext|>' + txt + '<|endoftext|>', truncation=True,
                                       max_length=max_length, padding="max_length")
            self.input_ids.append(torch.tensor(encodings_dict['input_ids']))
            self.attn_masks.append(torch.tensor(encodings_dict['attention_mask']))

    def __len__(self):
        return len(self.input_ids)

    def __getitem__(self, idx):
        return self.input_ids[idx], self.attn_masks[idx]

# pip install accelerate -U

training_args = TrainingArguments(output_dir='./results', num_train_epochs=1, logging_steps=100, save_steps=5000,
                                  per_device_train_batch_size=1, per_device_eval_batch_size=1,
                                  warmup_steps=10, weight_decay=0.05, logging_dir='../logs/gpt2_fine_tune', report_to = 'none')

def fine_tune_gpt2(df):
  # max_length = max([len(tokenizer.encode(description)) for description in descriptions])
  tweets = []
  max_length = 0
  for i in df.index:
    for j in range(50):
      try:
        max_length = max([max_length, len(tokenizer.encode(df[f"tweet_{j}"][i]))])
        tweets.append(df[f"tweet_{j}"][i])
      except:
        continue

  dataset = MBTIDataset(tweets, tokenizer, max_length=max_length)
  train_size = int(0.9 * len(dataset))
  train_dataset, val_dataset = random_split(dataset, [train_size, len(dataset) - train_size])
  Trainer(model=model,  args=training_args, train_dataset=train_dataset,
        eval_dataset=val_dataset, data_collator=lambda data: {'input_ids': torch.stack([f[0] for f in data]),
                                                              'attention_mask': torch.stack([f[1] for f in data]),
                                                              'labels': torch.stack([f[0] for f in data])}).train()

def generate_samples(model, pt):
  generated = tokenizer("<|startoftext|> ", return_tensors="pt").input_ids.cuda()
  sample_outputs = model.generate(generated, do_sample=True, top_k=50,
                                max_length=300, top_p=0.95, temperature=1.9, num_return_sequences=20)
  with open(f'../stats/{pt}_samples.pickle', 'wb') as handle:
    pickle.dump(sample_outputs, handle)

for t in types:
  tokenizer = GPT2Tokenizer.from_pretrained('gpt2-medium', bos_token='<|startoftext|>',
                                          eos_token='<|endoftext|>', pad_token='<|pad|>')
  model = GPT2LMHeadModel.from_pretrained('gpt2-medium').cuda()
  model.resize_token_embeddings(len(tokenizer))
  # model = torch.load(path + f"models/{t}.language_model.pt")
  df = data[data['type'] == t.upper()]
  df = df.reset_index()
  fine_tune_gpt2(df)
  generate_samples(model, t)
  torch.save(model, f"../models/{t}.language_model.pt")

