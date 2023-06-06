"""
Usage:
    crawl.py crawl1 --tweet_num=<argument> --consumer_key=<argument> --consumer_secret=<argument> --access_token=<argument> --access_token_secret=<argument> [options]
    crawl.py crawl2 --tweet_num=<argument> --consumer_key=<argument> --consumer_secret=<argument> --access_token=<argument> --access_token_secret=<argument> --personality_type=<argument> [options]    

Options:
    -h --help                               show this screen.
    --consumer_key=<argument>               consumer_key
    --consumer_secret=<argument>            consumer_secret
    --access_token=<argument>               access_token
    --access_token_secret=<argument>        access_token_secret 
    --personality_type=<argument>           personality type
    --tweet_num=<argument>                  number of tweets to crawl
"""

import tweepy
import pandas as pd
from colorama import Fore, Back, Style
from docopt import docopt


path_destination = "../data/raw/"

api_tokens = {
        "consumer_key": None,
        "consumer_secret" : None,
        "access_token" : None,
        "access_token_secret" : None,
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
    "ISTJ",
]


def crawling(api, tweet_num, personality_type=None):
    if personality_type:
        types = [personality_type]
    for t in types:
        print(f"Collecting tweets for {t} personality.")
        data_dict = {
            "user_id": [],
            # "user_id_str": [],
            "user_screen_name": [],
            "user_name": [],
            "text": [], 
            "personality_type": []
        }
        count = 0
        desired_count = tweet_num
        tweet_count = 0
        q = f'{t} -from:advertising_account -filter:statuses_min:25'
        for tweet in tweepy.Cursor(api.search_tweets, q=q, lang='en').items():
            if tweet_count >= desired_count:
                break
            if count % 100 == 0 and count != 0:
                print(f"In the {count}th iteration, {tweet_count} tweets have been collected.")
            count += 1
            user = api.get_user(user_id=tweet.user.id)
            if user.friends_count >= 50 and user.followers_count >= 50:
                data_dict['user_screen_name'].append(tweet.user.screen_name)
                data_dict['user_id'].append(tweet.user.id)
                # data_dict['user_id_str'].append(tweet.user.id_str)
                data_dict['user_name'].append(tweet.user.name)
                data_dict['text'].append(tweet._json['text'])  
                data_dict['personality_type'].append(t)
                tweet_count += 1
        data = pd.DataFrame(data_dict)
        print(f"End of collecting tweets for {t} personality")
        print("===============================================")
        data.to_csv(path_destination + f"{t}/{t}.csv")


def main():
    """ 
    Main func.
    """
    args = docopt(__doc__)
    
    for k in api_tokens.keys():
        api_tokens[k] = args[f"--{k}"]
    
    auth = tweepy.OAuthHandler(api_tokens["consumer_key"], api_tokens["consumer_secret"])
    auth.set_access_token(api_tokens["access_token"], api_tokens["access_token_secret"])
    api = tweepy.API(auth, wait_on_rate_limit=True)

    if args['crawl1']:
        crawling(api, int(args["--tweet_num"]))
    elif args['crawl2']:
        if args["--personality_type"]:
            if args["--personality_type"].upper() in types:
                pt = args["--personality_type"].upper()
            else:
                raise RuntimeError('invalid personality type')
        else:
            raise RuntimeError('enter a personality type')
        crawling(api, int(args["--tweet_num"]), pt)
    else:
        raise RuntimeError('invalid run mode')


if __name__ == '__main__':
    main()