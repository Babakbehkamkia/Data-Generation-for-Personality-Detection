@echo off
SETLOCAL ENABLEDELAYEDEXPANSION
rem    Run this file on the command line of an environment that contains "python" in path
rem    For example, in the terminal of your IDE
rem    Or in the correct environment of your anaconda prompt

set list="ENFJ" "ENFP" "ENTJ" "ENTP" "ESFJ" "ESFP" "ESTJ" "ESTP" "INFJ" "INFP" "INTJ" "INTP" "ISFJ" "ISFP" "ISTJ" "ISTP"

echo What do you want to do?
echo You have 3 options. Your options are:
echo 1. Collection of raw data
echo 2. Cleaning the collected data
echo 3. Extracting the statistics
echo 4. Generation of new data
echo 5. All together
set /p action= Please type the corresponding number:
echo You have chosen option %action%

if %action% == 1 (
    @REM python collect.py --tweet_num=100 --consumer_key=consumer_key --consumer_secret=consumer_secret --access_token=access_token --access_token_secret=access_token_secret
    echo Now, you should enter your Twitter API keys!
    set /p consumer_key= Please enter your consumer_key:
    set /p consumer_secret= Please enter your consumer_secret:
    set /p access_token= Please enter your access_token:
    set /p access_token_secret= Please enter your access_token_secret:

    echo Choose one of the followring options.
    echo 1. crawl for all personality types
    echo 2. crawl for an specific personality type
    set /p ct= Please enter the number of corresponding option:

    if !ct! == 1 (
        set /p tweet_num= Please enter your desired number of tweets that you want to extract for each personality type:
        python crawl.py cwawl1 --tweet_num=!tweet_num! --consumer_key=!consumer_key! --consumer_secret=!consumer_secret! --access_token=!access_token! --access_token_secret=!access_token_secret!
    ) else if !ct! == 2 (
        set /p pt_crawl= For which MBTI personality type you want to crawl?
        set /p tweet_num2= Determine the number of samples that you want to crawl for the !pt_crawl!:
        python crawl.py cwawl2 --tweet_num=!tweet_num2! --consumer_key=!consumer_key! --consumer_secret=!consumer_secret! --access_token=!access_token! --access_token_secret=!access_token_secret! --personality_type=!pt_crawl!
    ) else (
    echo Invalid Option Selected
    )

) else if %action% == 2 (
    echo In this section, you have 3 options:
    echo 1. Cleaning data
    echo 2. Breaking samples into words and sentences
    echo 3. Seeing some examples of cleaned data
    set /p cleaning_decision= Your decision:

    if !cleaning_decision! == 1 (
        echo You have chosen "Cleaning data"
        echo Now, you should choose the functions that you want to apply on data. [y/n]
        set /p remove_hashtag= Do you want to remove hashtags?
        set /p remove_usernames= Do you want to remove usernames?
        set /p remove_links= Do you want to remove links?
        set /p replacing_emojis= Do you want to replace emojis with their text form? note: if you choose "n", they will be removed.

        python cleaning.py clean --remove_hashtag=!remove_hashtag! --remove_usernames=!remove_usernames! --remove_links=!remove_links! --replacing_emojis=!replacing_emojis!
    ) else if !cleaning_decision! == 2 (
        echo You have chosen "Breaking"
        python cleaning.py break
    ) else if !cleaning_decision! == 3 (
        echo You have chosen "Seeing example"
        set /p ptype= Choose a personality type:
        python cleaning.py example --personality_type=!ptype!
    ) else (
    echo Invalid Option Selected
    )
    
) else if %action% == 3 (
    echo Now, you should determine that you want to extract the basic statistics of a personality type or extract the advanced statistics.
    echo 1. basic statistics
    echo 2. advanced statistics
    set /p type= Your decision:
    if !type! == 1 (
        echo You have chosen "basic statistics"
        @REM set /p pt= For which personality type you want to extract statistics?
        @REM python stats_file.py statistics --personality_type=!pt!
        python stats_file.py statistics
    ) else if !type! == 2 (
        echo You have chosen "advanced statistics"
        python stats_file.py advanced_statistics
    ) else (
    echo Invalid Option Selected
    )
) else if %action% == 4 (
    set /p key= First, please enter your OpenAI API key:
    echo Choose one of the followring options.
    echo 1. Generate samples for all personality types
    echo 2. Generate samples for an specific personality type
    set /p gt= Please enter the number of corresponding option:

    if !gt! == 1 (
        set /p gnum= Determine the number of samples that you want to generate for each personality type:
        python generate.py generate1 --sample_num=!gnum! --OpenAI_key=!key!
    ) else if !gt! == 2 (
        set /p gpt= For which MBTI personality type you want to generate data?
        set /p gnum2= Determine the number of samples that you want to generate for the !gpt!:
        python generate.py generate2 --sample_num=!gnum2! --personality_type=!gpt! --OpenAI_key=!key!
    ) else (
    echo Invalid Option Selected
    )

    python generate.py generate --train-src=./zh_en_data/train.zh --train-tgt=./zh_en_data/train.en --dev-src=./zh_en_data/dev.zh --dev-tgt=./zh_en_data/dev.en --vocab=vocab.json --lr=5e-5
) else if %action% == 5 (
    echo Crawling phase ...
    echo Now, you should enter your Twitter API keys!
    set /p consumer_key= Please enter your consumer_key:
    set /p consumer_secret= Please enter your consumer_secret:
    set /p access_token= Please enter your access_token:
    set /p access_token_secret= Please enter your access_token_secret:
    echo Now, please enter your desired number of tweets that you want to extract for each personality type.
    set /p tweet_num= Please enter the number:
    python crawl.py cwawl1 --tweet_num=!tweet_num! --consumer_key=!consumer_key! --consumer_secret=!consumer_secret! --access_token=!access_token! --access_token_secret=!access_token_secret!

    echo Cleaning data ...
    echo Now, you should choose the functions that you want to apply on data. [y/n]
    set /p remove_hashtag= Do you want to remove hashtags?
    set /p remove_usernames= Do you want to remove usernames?
    set /p remove_links= Do you want to remove links?
    set /p replacing_emojis= Do you want to replace emojis with their text form? note: if you choose "n", they will be removed.

    python cleaning.py clean --remove_hashtag=!remove_hashtag! --remove_usernames=!remove_usernames! --remove_links=!remove_links! --replacing_emojis=!replacing_emojis!
    
    echo Breaking phase ...
    python cleaning.py break

    echo Extracting basic statistics ...
    @REM for %%t in (%list%) do (
    @REM     @REM echo %%t
    @REM     python stats_file.py statistics --personality_type=%%t
    @REM )
    python stats_file.py statistics

    echo Extracting advanced statistics ...
    python stats_file.py advanced_statistics



@REM ) else if "%1%"=="test_local" (
@REM     set CUDA_VISIBLE_DEVICES=0 & python run.py decode model.bin ./zh_en_data/test.zh ./zh_en_data/test.en outputs/test_outputs.txt
@REM ) else if "%1%"=="train_debug" (
@REM     python run.py train --train-src=./zh_en_data/train_debug.zh --train-tgt=./zh_en_data/train_debug.en --dev-src=./zh_en_data/dev.zh --dev-tgt=./zh_en_data/dev.en --vocab=vocab.json --lr=5e-5
@REM ) else if "%1%"=="vocab" (
@REM     python vocab.py --train-src=./zh_en_data/train.zh --train-tgt=./zh_en_data/train.en vocab.json
) else (
    echo Invalid Option Selected
)
