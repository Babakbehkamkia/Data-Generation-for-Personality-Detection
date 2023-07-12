#!/bin/bash

listVar="ENFJ ENFP ENTJ ENTP ESFJ ESFP ESTJ ESTP INFJ INFP INTJ INTP ISFJ ISFP ISTJ ISTP"

echo "What do you want to do?"
echo "You have 3 options. Your options are:"
echo "1. Collection of raw data"
echo "2. Cleaning the collected data"
echo "3. Extracting the statistics"
echo "4. Generation of new data"
echo "5. All together"
read -p "Please type the corresponding number: " action
echo "You have chosen option ${action}"

if [ "$action" = "1" ]; then
	echo "Now, you should enter your Twitter API keys!"
    read -p "Please enter your consumer_key: " consumer_key
    read -p "Please enter your consumer_secret: " consumer_secret
    read -p "Please enter your access_token: " access_token
    read -p "Please enter your access_token_secret: " access_token_secret
    
    echo "Choose one of the following options."
    echo "1. crawl for all personality types"
    echo "2. crawl for an specific personality type"
    read -p "Please enter the number of corresponding option: " ct

    
    if [ "$ct" = "1" ]; then
        read -p "Please enter your desired number of tweets that you want to extract for each personality type: " tweet_num
        python3 crawl.py crawl1 --tweet_num=$tweet_num --consumer_key=$consumer_key --consumer_secret=$consumer_secret --access_token=$access_token --access_token_secret=$access_token_secret
    elif [ "$ct" = "2" ]; then
        read -p "For which MBTI personality type you want to crawl? " pt_crawl
        read -p "Determine the number of samples that you want to crawl for the ${pt_crawl}: " tweet_num2
        python3 crawl.py crawl2 --tweet_num=$tweet_num2 --consumer_key=$consumer_key --consumer_secret=$consumer_secret --access_token=$access_token --access_token_secret=$access_token_secret --personality_type=$pt_crawl
    else
        echo "Invalid Option Selected"
    fi

elif [ "$action" = "2" ]; then
    echo "In this section, you have 3 options:"
    echo "1. Cleaning data"
    echo "2. Breaking samples into words and sentences"
    echo "3. Seeing some examples of cleaned data"
    read -p "Your decision: " cleaning_decision

    if [ "$cleaning_decision" = "1" ]; then
        echo "You have chosen "Cleaning data""
        echo "Now, you should choose the functions that you want to apply on data. [y/n]"
        
        read -p "Do you want to remove hashtags? " remove_hashtag
        read -p "Do you want to remove usernames? " remove_usernames
        read -p "Do you want to remove links? " remove_links
        read -p "Do you want to replace emojis with their text form? note: if you choose 'n', they will be removed. " replacing_emojis
        python3 cleaning.py clean --remove_hashtag=$remove_hashtag --remove_usernames=$remove_usernames --remove_links=$remove_links --replacing_emojis=$replacing_emojis
    elif [ "$cleaning_decision" = "2" ]; then
        echo "You have chosen "Breaking""
        python3 cleaning.py break
    elif [ "$cleaning_decision" = "3" ]; then
        echo "You have chosen "Seeing example""
        read -p "Choose a personality type: " ptype
        python3 cleaning.py example --personality_type=$ptype
    else
        echo "Invalid Option Selected"
    fi
elif [ "$action" = "3" ]; then
    echo "Now, you should determine that you want to extract the basic statistics of a personality type or extract the advanced statistics."
    echo "1. basic statistics"
    echo "2. advanced statistics"
    read -p "Your decision " type

    if [ "$type" = "1" ]; then
        echo "You have chosen "basic statistics""
        # read -p "For which personality type you want to extract statistics? " pt
        # python3 stats_file.py statistics --personality_type=$pt
        python3 stats_file.py statistics
    elif [ "$type" = "2" ]; then
        echo "You have chosen "advanced statistics""
        python3 stats_file.py advanced_statistics

    else
        echo "Invalid Option Selected"
    fi

elif [ "$action" = "4" ]; then
    read -p "First, please enter your OpenAI API key: " key
    echo "Choose one of the following options."
    echo "1. Generate samples for all personality types"
    echo "2. Generate samples for an specific personality type"
    read -p "Please enter the number of corresponding option: " gt

    if [ "$gt" = "1" ]; then
        read -p "Determine the number of samples that you want to generate for each personality type: " gnum
        python3 generate.py generate1 --sample_num=$gnum --OpenAI_key=$key
    elif [ "$gt" = "2" ]; then
        read -p "For which MBTI personality type you want to generate data? " gpt
        read -p "Determine the number of samples that you want to generate for the ${gpt}: " gnum2
        python3 generate.py generate2 --sample_num=$gnum2 --personality_type=$gpt --OpenAI_key=$key
    else
        echo "Invalid Option Selected"
    fi
elif [ "$action" = "5" ]; then
    echo "Crawling phase ..."
    echo "Now, you should enter your Twitter API keys!"
    read -p "Please enter your consumer_key: " consumer_key
    read -p "Please enter your consumer_secret: " consumer_secret
    read -p "Please enter your access_token: " access_token
    read -p "Please enter your access_token_secret: " access_token_secret
    echo "Now, please enter your desired number of tweets that you want to extract for each personality type."
    read -p "Please enter the number: " tweet_num
    python3 collect.py --tweet_num=$tweet_num --consumer_key=$consumer_key --consumer_secret=$consumer_secret --access_token=$access_token --access_token_secret=$access_token_secret

    echo "Cleaning data ..."
    echo "Now, you should choose the functions that you want to apply on data. [y/n]"
    read -p "Do you want to remove hashtags? " remove_hashtag
    read -p "Do you want to remove usernames? " remove_usernames
    read -p "Do you want to remove links? " remove_links
    read -p "Do you want to replace emojis with their text form? note: if you choose 'n', they will be removed. " replacing_emojis
    python3 cleaning.py clean --remove_hashtag=$remove_hashtag --remove_usernames=$remove_usernames --remove_links=$remove_links --replacing_emojis=$replacing_emojis

    echo "Breaking phase ..."
    python3 cleaning.py break

    echo "Extracting basic statistics ..."
    # for t in $listVar; do
    #     echo "$t"
    #     python3 stats_file.py statistics --personality_type=$t
    # done
    python3 stats_file.py statistics

    echo "Extracting advanced statistics ..."
    python3 stats_file.py advanced_statistics
else
	echo "Invalid Option Selected"
fi