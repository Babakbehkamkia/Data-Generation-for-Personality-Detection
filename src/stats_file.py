
"""
Usage:
    stats_file.py statistics [options]
    stats_file.py advanced_statistics [options]

Options:
    -h --help                               show this screen.
"""


import pandas as pd
import re
from colorama import Fore, Back, Style
from docopt import docopt
import matplotlib.pyplot as plt
from sklearn.feature_extraction.text import TfidfVectorizer
import numpy as np
import nltk 
nltk.download('punkt')

import sys
sys.path.insert(1, '../src')
from cleaning import *

path_datasets = "../data/clean/"
path_destination = "../stats/"

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

def basic_statistics():
    main_df = pd.DataFrame(index=types, columns=["sample num", "sentence num", "word num", "unique word num"])
    for t in types:
        df = pd.read_csv(path_datasets + f"{t}/{t}.csv")
        unique_words = {}
        
        print(f"Basic statistics for {t}: ")
        
        print(Fore.GREEN + f"number of samples: {df.shape[0]}")
        main_df.loc[t, "sample num"] = df.shape[0]
        
        df['words'] = df.apply(lambda x: extract_word(x, unique_words, []), axis=1)
        df['word_count'] = df.apply(extract_word_count, axis=1)
        df['sentences'] = df.apply(extract_sentence, axis=1)
        df['sentence_count'] = df.apply(extract_sentence_count, axis=1)
        
        print(f"number of sentences: {sum(df['sentence_count'])}")
        main_df.loc[t, "sentence num"] = sum(df['sentence_count'])
        
        print(f"number of word: {sum(df['word_count'])}")
        main_df.loc[t, "word num"] = sum(df['word_count'])
        
        print(f"number of unique word: {len(unique_words.keys())}")
        main_df.loc[t, "unique word num"] = len(unique_words.keys())
        
        print(Style.RESET_ALL)
    main_df.to_csv(path_destination + "basic_statistics.csv")

def extract_word(row, unique_words, all_texts):
    text = row['cleaned_text']
    if type(text) != str:
        all_texts.append("")
        return []
    all_texts.append(text)
    words= nltk.word_tokenize(text)
    for word in words:
        if word not in unique_words:
            unique_words[word] = 0
        unique_words[word] += 1
    return words

def extract_sentence(row):
    text = row['cleaned_text']
    if type(text) != str:
        return []
    sentences = nltk.sent_tokenize(text)
    return sentences

def extract_word_count(row):
    words = row['words']
    return len(words)

def extract_sentence_count(row):
    words = row['sentences']
    return len(words)

def mergeDictionary(dict_1, dict_2):
    dict_3 = {**dict_1, **dict_2}
    for key, value in dict_3.items():
        if key in dict_1 and key in dict_2:
                dict_3[key] = value + dict_1[key]
    return dict_3

def all_func():
    freq_dict = {}
    all_texts = []
    all_dicts = {}
    for t in types:
        unique_words = {}
        texts = []
        df = pd.read_csv(path_datasets + f"{t}/{t}.csv")
        df['words'] = df.apply(lambda x: extract_word(x, unique_words, texts), axis=1)
        df['sentences'] = df.apply(extract_sentence, axis=1)

        freq_dict = mergeDictionary(freq_dict, unique_words)
        all_dicts[t] = unique_words
        all_texts.append(" ".join(texts))
    return all_dicts, freq_dict, all_texts

def draw_plots(words_dict):
    sorted_words_dict = sorted(words_dict.items(), key=lambda x:x[1], reverse=True)
    names = []
    values = []
    for i in range(20):
        names.append(sorted_words_dict[i][0])
        values.append(sorted_words_dict[i][1])

    plt.bar(range(20), values, tick_label=names)
    plt.title(f"most frequent words in tweets", fontweight ="bold")
    plt.xticks(rotation=45, ha='right')
    plt.savefig(path_destination + "frequency.png")

def compute_tf_idf(all_texts, types):
    vectorizer = TfidfVectorizer()
    tfidf_matrix = vectorizer.fit_transform(all_texts)
    feature_names = np.array(vectorizer.get_feature_names_out())

    num_popular_word = 20
    popular_words_indices = np.argsort(tfidf_matrix.toarray(), axis=1)[:, -num_popular_word:]

    freq_on_labels = {}
    for i in range(len(types)):
        tf_idf_list = list(feature_names[popular_words_indices[i]])
        freq_on_labels[types[i]] = {f"{index}": tf_idf_list[index] for index in range(len(tf_idf_list))}

    # df = pd.DataFrame.from_dict(freq_on_labels, orient="index")
    df = pd.DataFrame(freq_on_labels)
    df.to_csv(path_destination + "tf-idf.csv")

def find_common_words(dict1, dict2):
    common_words = []
    dict1 = set(dict1)
    dict2 = set(dict2)
    for name in dict1.intersection(dict2):
        common_words.append(name)
    return common_words

def update_dataframe(pt1, pt2, dict1, dict2, common_words, df):
    uncommon = {}
    for word in dict1:
        if word not in common_words:
            uncommon[word] = dict1[word]
    sorted_not_common = sorted(uncommon.items(), key=lambda x:x[1], reverse=True)
    selected_words = sorted_not_common[:10]
    # df.loc[pt1, pt2] = sorted_not_common[:10]
    for i in range(10):
        df.loc[f"{pt1}/{pt2}", f"word {i}"] = selected_words[i][0]
        # df.loc[f"{pt1}/{pt2}", f"num {i}"] = selected_words[i][1]
    return len(uncommon.keys())

def compute_common_uncommon(all_dicts, types):
    all_common_words = {}
    common_number = pd.DataFrame(index=types, columns=types)
    uncommon_number = pd.DataFrame(index=types, columns=types)
    df = pd.DataFrame(columns=[f"word {i}" for i in range(10)])
    for i in range(16):
        for j in range(i+1, 16):
            pt1 = types[i]
            pt2 = types[j]
            dict1 = all_dicts[pt1]
            dict2 = all_dicts[pt2]
            common_words = find_common_words(dict1, dict2)
            all_common_words[f"{pt1}/{pt2}"] = common_words
            all_common_words[f"{pt2}/{pt1}"] = common_words
            
            common_words_num = len(common_words)
            
            common_number.loc[pt1, pt2] = common_words_num
            common_number.loc[pt2, pt1] = common_words_num
            
            pt1_uncommon_number = update_dataframe(pt1, pt2, dict1, dict2, common_words, df)
            pt2_uncommon_number = update_dataframe(pt2, pt1, dict2, dict1, common_words, df)
            
            uncommon_number.loc[pt1, pt2] = pt1_uncommon_number + pt2_uncommon_number
            uncommon_number.loc[pt2, pt1] = pt1_uncommon_number + pt2_uncommon_number
    df.iloc[:20].to_csv(path_destination + "most_frequent_uncommon.csv", index=True)
    
    common_number.to_csv(path_destination + "number_of_common_words.csv")
    uncommon_number.to_csv(path_destination + "number_of_uncommon_words.csv")
    return all_common_words

def compute_RNF(all_dicts, all_common_words, types):
    df = pd.DataFrame(columns=[f"word {i}" for i in range(10)])
    for i in range(16):
        for j in range(i+1, 16):
            pt1 = types[i]
            pt2 = types[j]
            dict1 = all_dicts[pt1]
            dict2 = all_dicts[pt2]
            relative_normalized_frequency = {}
            total_first_pt_word_num = sum(dict1.values())
            total_second_pt_word_num = sum(dict2.values())
            common_words = all_common_words[f"{pt1}/{pt2}"]
            for word in common_words:
                up = dict1[word] / total_first_pt_word_num
                down = dict2[word] / total_second_pt_word_num
                relative_normalized_frequency[word] = round((up / down), 2)
            
            sorted_rel_freq = sorted(relative_normalized_frequency.items(), key=lambda x:x[1], reverse=True)
            for index in range(10):
                df.loc[f"{pt1}/{pt2}", f"word {index}"] = sorted_rel_freq[index][0]
                # df.loc[f"{pt1}/{pt2}", f"num {index}"] = sorted_rel_freq[index][1]
            # df[pt2, pt1] = sorted_rel_freq[:10]
    df.iloc[:20].to_csv(path_destination + "RNF.csv")


def main():
    """ 
    Main func.
    """
    args = docopt(__doc__)

    if args['advanced_statistics']:
        all_dicts, freq_dict, all_texts = all_func()
        draw_plots(freq_dict)
        print(Fore.GREEN + "plot done!")
        compute_tf_idf(all_texts, types)
        print("tf_idf done")
        all_common_words = compute_common_uncommon(all_dicts, types)
        compute_RNF(all_dicts, all_common_words, types)
        print("all done!")
        print(Style.RESET_ALL)
        
    elif args['statistics']:
        basic_statistics()
    else:
        raise RuntimeError('invalid run mode')


if __name__ == '__main__':
    main()