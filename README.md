# [WIP] stweet

![Python package](https://github.com/markowanga/stweet/workflows/Python%20package/badge.svg?branch=master)
[![codecov](https://codecov.io/gh/markowanga/stweet/branch/master/graph/badge.svg?token=1PV6VC8HRF)](https://codecov.io/gh/markowanga/stweet)


Modern fast python library to quickly scrap tweets from Twitter unofficial API.

This tool helps you to scrap tweet by search phrase. It uses the twitter api, same api is used on website.

## Inspiration for the creation of the library
I have used twint to scrap tweets, but it have many errors it doesn't work correct. 
The code was not simple to understand. All tasks have one config and user must know what exactly parameter is.
Last important thing is fact that api can change — Twitter is api owner and changes are dependent of them. 
It is annoying when something does not work and users must report bugs is issues.

## Main advantages of the library
 - **Simple code** — code is not mine, every user can contribute library
 - **Domain objects and interfaces** — main part of functionalities can be replaced (eg. calling web requests),
   library have basic simple solution, if you want to expand it you can do it very simple
 - **100% coverage with integration tests** — this can find the api changes, 
   tests is run every week and when task is failed we can easily find the source of change
 - **Custom tweets output** — it's part of interface, it you want to save custom tweets it takes you a short moment

## Basic usage
To make simple request the scrap **task** must be prepared. Next task should be processed by **runner**.
```python
import stweet as st

search_tweets_task = st.SearchTweetsTask(
    all_words='#covid19',
    tweets_count=5
)

tweets_collector = st.CollectorTweetOutput()

st.TweetSearchRunner(
    search_tweets_task=search_tweets_task,
    tweet_outputs=[tweets_collector, st.CsvTweetOutput('output_file.csv')]
).run()

tweets = tweets_collector.get_scrapped_tweets()
```
This simple code snippet call for all tweets with hashtag **#covid19**.
As a result in tweets object in the list are scrapped tweets. 
All important things about task and runner will be describe below.

## SearchTweetsTask
This class represent the task to scrap tweets. Contain this properties:

|Property|Type|Default value|Description|
|---|---|---|---|
|all_words|Optional[str]|None|Search for tweets having all words in this property|
|exact_words|Optional[str]|None|Search for tweets with exacting words in this property|
|any_word|Optional[str]|None|Search for tweets with any words in this property|
|from_username|Optional[str]|None|Search for tweets from username|
|to_username|Optional[str]|None|Search for tweets to username (tweets starts from mention to user)|
|since|Optional[Arrow]|None|Search for tweets since time|
|until|Optional[Arrow]|None|Search for tweets until time|
|language|Optional[st.Language]|None|Search for tweets with language|
|tweets_count|Optional[int]|None|Search first tweets_count tweets|
|replies_filter|Optional[st.RepliesFilter]|None|Filter tweets with reply/original status|

All properties came from **Twitter advanced search** and are default None.

## SearchRunner
With this runner library can scrap tweets specified in SearchTweetsTask.
Runner have properties:

|Property|Type|Default value|Description|
|---|---|---|---|
|search_run_context|st.SearchRunContext|None, in \_\_init\_\_() assign SearchRunContext()|Search context, contains all important properties to make next request to Twitter|
|search_tweets_task|st.SearchTweetsTask|**Obligatory property**|Task specify which tweets runner should download|
|tweet_outputs|List[st.TweetOutput]|**Obligatory property**|List of objects to export downloaded tweets|
|web_client|st.WebClient|stweet.http_request.WebClientRequests|Implementation of web client, can be replaced for custom implementation|
|tweet_parser|st.TweetParser|stweet.parse.TwintBasedTweetParser|Parser of tweets from web api response|
