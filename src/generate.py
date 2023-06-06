# !pip install -q openai



"""
Usage:
    generate.py generate1 --sample_num=<argument> --OpenAI_key=<argument> [options]
    generate.py generate2 --sample_num=<argument> --personality_type=<argument> --OpenAI_key=<argument> [options]    

Options:
    -h --help                               show this screen.
    --sample_num=<argument>                 the number of generated samples
    --OpenAI_key=<argument>                 the API key of OpenAI
    --personality_type=<argument>           personality type
"""


import json
import pandas as pd
import numpy as np
import zipfile
from tqdm import tqdm
import time
import openai
import random
from colorama import Fore, Back, Style
from docopt import docopt
import sys

sys.path.insert(1, '../src')
from stats_file import *

import nltk 
nltk.download('punkt')

path_datasets = "../data/raw/"

# data = pd.read_csv(path_datasets + "mbti_1.csv")

def extracting_tweet(row):
  tweets = row['posts'].split("|||")
  for i in range(50):
    row[f'tweet_{i}'] = None
    if i < len(tweets):
      row[f'tweet_{i}'] = tweets[i]
  return row

#data = data.apply(extracting_tweet, axis=1)

#data.to_csv(path_datasets + "mbti_tweets.csv")

data = pd.read_csv(path_datasets + "mbti_tweets.csv")

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
    "ISTJ",
]

samples = {
    "type": [],
    "topic": [],
    "post": []
}
topic_list = ["movies", "cinema", "parties", "book", "love", "depression"]

def masking_type(text):
  words= nltk.word_tokenize(text)
  for index in range(len(words)):
    if words[index] in types:
      words[index] = "[PT]"
  return " ".join(words)


def generation(sample_num, personality_types=None):
  if personality_types:
    types = [personality_types]
  for index in tqdm(range(len(types))):
    t = types[index]
    messages = [ {"role": "system", "content":
              "You are a intelligent assistant."} ]
    
    for i in range(sample_num):
      if i % 10 == 0:
        messages = [ {"role": "system", "content":
              "You are a intelligent assistant."} ]
      if i % 3 == 0:
        time.sleep(61)
      topic_num = random.randint(0, len(topic_list)-1)
      topic = topic_list[topic_num]

      mini_data = data[data['type'] == f"{t}"]
      total_size = mini_data.shape[0]
      row_num = random.randint(0, total_size-1)
      tweet_num = random.randint(0, 49)
        
      try:
        prompt = f'''Your task is to generate a human written post. Do not mention that your are an intelligent assistant
                    the generated post must be by a person with the given personality. Do not mention the given personality directly.
                    The generated post must discuss about the given topic in some point of itself. 
                    the post should not be more than 50 words.
                    just return the post.
                    personality: {t}
                    topic: {topic}

                    Here is an example post, but we do not know the topic of the text blow. you can learn from its structure to understand how a person with the given personality think.
                    text: ```{mini_data.iloc[row_num][f"tweet_{tweet_num}"]}```'''
        
          
        message = prompt
        if message:
          messages.append(
            {"role": "user", "content": message},
          )
          chat = openai.ChatCompletion.create(
            model="gpt-3.5-turbo", messages=messages
          )
        reply = chat.choices[0].message.content

        samples['post'].append(masking_type(reply))
        samples['type'].append(t)
        samples['topic'].append(topic)
        
        messages.append({"role": "assistant", "content": reply})
      except Exception as e: 
        print(e)
        samples['post'].append("error")
        samples['type'].append(t)
        samples['topic'].append(topic)
        print("There is an error in : ", i)

  generated_data = pd.DataFrame(samples)
  if personality_types:
    generated_data.to_csv(path_datasets + f"generated_data_{personality_types}.csv")
  else:
    generated_data.to_csv(path_datasets + "generated_data.csv")


def main():
    """ 
    Main func.
    """
    args = docopt(__doc__)
    
    openai.api_key = args["--OpenAI_key"]

    if args['generate1']:
        generation(int(args["--sample_num"]))
    elif args['generate2']:
        if args["--personality_type"]:
            if args["--personality_type"].upper() in types:
                pt = args["--personality_type"].upper()
            else:
                raise RuntimeError('invalid personality type')
        else:
            raise RuntimeError('invalid personality type')
        print(f"Generating {args['--sample_num']} examples for {pt} personality type.")
        generation(int(args["--sample_num"]), pt)
    else:
        raise RuntimeError('invalid run mode')


if __name__ == '__main__':
    main()

