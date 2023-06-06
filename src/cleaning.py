# !pip install colorama
# !pip install demoji
# !pip install clean-text
# !pip install docopt
# !pip install matplotlib

"""
Usage:
    cleaning.py clean --remove_hashtag=<argument> --remove_usernames=<argument> --remove_links=<argument> --replacing_emojis=<argument> [options]
    cleaning.py example --personality_type=<argument> [options]
    cleaning.py break [options]
    

Options:
    -h --help                               show this screen.
    --remove_hashtag=<argument>             boolean for removing hashtags
    --remove_usernames=<argument>           boolean for removing usernames
    --remove_links=<argument>               boolean for removing links
    --replacing_emojis=<argument>           boolean for replacing emojis 
    --personality_type=<argument>           personality type
"""

import pandas as pd
import re
from colorama import Fore, Back, Style
from cleantext import clean as emoji_remover
from docopt import docopt
import demoji
demoji.download_codes()

import matplotlib.pyplot as plt
from sklearn.feature_extraction.text import TfidfVectorizer
import numpy as np
import random
import nltk 
nltk.download('punkt')
nltk.download('stopwords')
nltk.download('wordnet')
nltk.download('omw-1.4')

from nltk.corpus import stopwords
from nltk.tokenize import TweetTokenizer
from nltk.stem import WordNetLemmatizer

import sys
sys.path.insert(1, '../stats')
from stats_file import *

path_datasets = "../data/raw/"
path_destination = "../data/clean/"

config = {
    "remove_hashtag" : False,
    "remove_usernames" : False,
    "remove_links" : False,
    "replacing_emojis" : False,
}


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



def remove_hashtags(text):
  cleaned_text = re.sub(r'#\w+\b', '', text)
  cleaned_text = re.sub(r'\s+', ' ', cleaned_text.strip())
  return cleaned_text

def remove_usernames(text):
  cleaned_text = re.sub(r'@\w+\b', '', text)
  cleaned_text = re.sub(r'\s+', ' ', cleaned_text.strip())
  return cleaned_text

def remove_links(text):
  cleaned_text = re.sub(r'http\S+|www\S+', '', text)
  cleaned_text = re.sub(r'\s+', ' ', cleaned_text.strip())
  return cleaned_text

def remove_retweet_sign(text):
  cleaned_text = text.replace("RT : ", '')
  return cleaned_text

def replace_emojis(text):
  text = demoji.replace_with_desc(text)
  text = text.replace(':', '')
  return text

def necessary_cleaning(text):

  text = re.sub(r"[^\w\s]", "", text)
  tokenizer = TweetTokenizer(preserve_case=False, strip_handles=True, reduce_len=True)
  tokens = tokenizer.tokenize(text)
  
  stop_words = set(stopwords.words("english"))
  tokens = [token for token in tokens if token not in stop_words]
  
  lemmatizer = WordNetLemmatizer()
  tokens = [lemmatizer.lemmatize(token) for token in tokens]
  
  cleaned_text = " ".join(tokens)
  return cleaned_text


def cleaning_tweets(row):
  text = row['text']
  if config["remove_hashtag"]:
    text = remove_hashtags(text)
  if config["remove_links"]:
    text = remove_links(text)
  if config["remove_usernames"]:
    text = remove_usernames(text)
  if config["remove_retweet_sign"]:
    text = remove_retweet_sign(text)
  if config["replacing_emojis"]:
    text = replace_emojis(text)
  else:
    text = emoji_remover(text, no_emoji=True)
  text = necessary_cleaning(text)
  return text

def print_sample(df):
  randomlist = random.sample(range(0, 100), 10)
  for item in randomlist:
    print(Fore.RED + "the actual text:\n")
    print(Style.RESET_ALL)
    print(df.iloc[item]['text'], "\n")
    print(Fore.GREEN + "the cleaned text:\n")
    print(Style.RESET_ALL)
    print(df.iloc[item]['cleaned_text'])
    print("\n============================\n")


def word_broken(pt, df):
    words_df = df[['user_id', 'user_screen_name', 'user_name', 'words', 'personality_type']]
    words_df.to_csv(f"../data/wordbroken/{pt}/{pt}.csv")

def sentence_broken(pt, df):
    words_df = df[['user_id', 'user_screen_name', 'user_name', 'sentences', 'personality_type']]
    words_df.to_csv(f"../data/sentencebroken/{pt}/{pt}.csv")

def broken():
    for t in types:
        print(f"breaking {t} into words and sentences ...")
        df = pd.read_csv(path_destination + f"{t}/{t}.csv")
        df['words'] = df.apply(lambda x: extract_word(x, {}, []), axis=1)
        df['sentences'] = df.apply(extract_sentence, axis=1)
        word_broken(t, df)
        sentence_broken(t, df)
        print(Fore.GREEN + f"{t} breaking done!\n")
        print(Style.RESET_ALL)

def main_cleaning():
    for t in types:
        print(f"cleaning {t} ...")
        df = pd.read_csv(path_datasets + f"{t}/{t}.csv")
        df['cleaned_text'] = df.apply(cleaning_tweets, axis=1)
        df.to_csv(path_destination + f"{t}/{t}.csv")
        print(Fore.GREEN + f"{t} cleaning done!\n")
        print(Style.RESET_ALL)


def main():
    """ 
    Main func.
    """
    args = docopt(__doc__)

    if args['clean']:
        for k in config.keys():
            if args[f"--{k}"].lower() == 'y':
                config[k] = True
            elif args[f"--{k}"].lower() == 'n':
                config[k] = False
            else:
                print(Fore.RED + f"Invalid input for --{k}")
                print(Style.RESET_ALL)
        config["remove_retweet_sign"] = True
        main_cleaning()
    elif args['example']:
        if args["--personality_type"]:
            if args["--personality_type"].upper() in types:
                pt = args["--personality_type"].upper()
            else:
                raise RuntimeError('invalid personality type')
        else:
            n = random.randint(10,15)
            pt = types[n]
        df = pd.read_csv(path_destination + f"{pt}/{pt}.csv")
        print(f"Here 10 examples of {pt} personality type.")
        print_sample(df)
    elif args['break']:
        broken()
    else:
        raise RuntimeError('invalid run mode')


if __name__ == '__main__':
    main()