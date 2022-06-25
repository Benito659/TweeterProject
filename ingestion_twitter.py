#### Import packages

from cgi import print_arguments
from http.client import UNAUTHORIZED
import json
import re
import requests
import tweepy
import os


#### Defining variables and credentials
consumer_key = "zuBhiUfuKbOWiQUrQOoUsbzyR"
consumer_secret = "xQ5YY3dJbNZLHVUZXCEkG7val1mDN1r7MluwkBTvPTRrAzCiGP"
access_token = "1264225213161619457-u8ZEceXQe3w7VnMpVwbd1L3W7mc47n"
access_token_secret = "3t6tVwofOJYP3oXfG8cae19VgjJssePmSppd6lN76Mu7y"
BEARER_TOKEN = 'AAAAAAAAAAAAAAAAAAAAAHmTawEAAAAAjTsiKpHQ3VFPzJCf05VQmFrjycs%3DzTSJfV7MwZIMTUAtSvIhB4YHieZ4XQxTrVz9HAGv74bGhwfcB1'

headers = {
    'Authorization': f"Bearer {BEARER_TOKEN}",
}
auth = tweepy.OAuth1UserHandler(consumer_key, consumer_secret, access_token, access_token_secret)
api = tweepy.API(auth)

try :
    api.verify_credentials()
except UNAUTHORIZED :
    print("l'autentification a echoué")


listFilms=[
    (['#ShangChi'],'https://twitter.com/MarvelFR/status/1384142929942368264','1384142929942368264',"https://www.youtube.com/watch?v=8YjFbMbfXaQ","8YjFbMbfXaQ"),
    (['#TheFalconandtheWinterSoldier'],'https://twitter.com/MarvelFR/status/1385509857223192577','1385509857223192577',"https://www.youtube.com/watch?v=X_mSpyPVVzk","X_mSpyPVVzk"),
    (['#LesEternels'],'https://twitter.com/MarvelFR/status/1396818114147409921','1396818114147409921',"https://www.youtube.com/watch?v=x_me3xsvDgk","x_me3xsvDgk"),
    (['#DoctorStrange'],'https://twitter.com/MarvelFR/status/1524434169232723971','1524434169232723971',"https://www.youtube.com/watch?v=aWzlQ2N6qqg","aWzlQ2N6qqg")
]



def recupInfosTweet(idTweet):
    params = {
        'ids': idTweet,
        'expansions':'author_id',
        'tweet.fields':'referenced_tweets',
        'tweet.fields':'public_metrics',
    }
    response = requests.get('https://api.twitter.com/2/tweets', params=params, headers=headers)
    #print(response.json()['data'])
    return response.json()['data'][0]


def recupListTweetCites(hastagList):
    listToReturn=[]
    for hastag in hastagList:
        tweets = api.search_tweets(hastag, tweet_mode="extended")
        listToReturn.extend([tweet.full_text for tweet in tweets])
    
    return listToReturn


def recupQuotedTweets(idTweet):
    params = {
        'max_results':100
    }
    response = requests.get('https://api.twitter.com/2/tweets/{}/quote_tweets'.format(idTweet),params=params, headers=headers)
    #print(response.json()['data'])
    return response.json()['data']




def processResult(tupleTree):
    resultInfos=recupInfosTweet(tupleTree[2])
    listTweetHastag=recupListTweetCites(tupleTree[0])
    listTweetReponse=recupQuotedTweets(tupleTree[2])
    youtubeDictionnaire=ingestionYoutube(tupleTree[4])
    #print(resultInfos)
    resultInfos.update({'tweetsHastag':listTweetHastag})
    #print(listTweetHastag)
    resultInfos.update({'tweetsResponse':listTweetReponse})
    #print(listTweetReponse)
    resultInfos.update({'youtubeResult':youtubeDictionnaire})  
    #print(resultInfos)
    return resultInfos

def recupToutTweets(listFilms):

    collectionList=[]
    for i in listFilms:
        collectionList.append(processResult(i))
    
    return collectionList


#Ingestion


def ingestionYoutube(video_id):
    from googleapiclient.discovery import build
    import json
    api_key ="AIzaSyDnyrf-muwJ5OuKzoFaVD_PmLPDMH5Iz8w"
    #video_id= "aWzlQ2N6qqg"

    resource = build('youtube', 'v3', developerKey=api_key)

    request1 = resource.videos().list(part="statistics", id=video_id)
    
    response1=request1.execute()

    items1=response1["items"][:1000]
    #print(json.dumps(items1[0]["statistics"]))

    resultToStock={}
    resultToStock.update({"statistics":items1})

    request = resource.commentThreads().list( part="snippet",videoId=video_id,maxResults= 10000, order="relevance") 
    response =request.execute()

    
    items = response["items"][:10000]
    list_commentaires=[]
    for item in items:
        item_info = item["snippet"]
        topLevelComment = item_info["topLevelComment"]
        comment_info = topLevelComment["snippet"]
        list_commentaires.append(
            {
                "Comment By:":comment_info["authorDisplayName"],
                "Comment Text:":comment_info["textDisplay"],
                "Likes on Comment:":comment_info["likeCount"],
                "Comment Date: ": comment_info['publishedAt']
            }
        )

    resultToStock.update({"Commentaires":list_commentaires})

    return resultToStock








def get_database(jsonRequest):
    from pymongo import MongoClient
    import pymongo

    # Create a connection using MongoClient. You can import MongoClient or use pymongo.MongoClient
    from pymongo import MongoClient
    client = MongoClient('localhost', port=8084)
    # Create a new collection
    db_name = client["tweet_information_db"]
    mycol = db_name["tweeteryoutubecollection"]

    mycol.insert_many(jsonRequest)
    
    

if __name__ == "__main__":    
    
    # Get the database
    #dbname = get_database()
    #collection_name = dbname["user_1_items"]
    #processResult((['#DoctorStrange'],'https://twitter.com/MarvelFR/status/1524434169232723971','1524434169232723971',"https://www.youtube.com/watch?v=aWzlQ2N6qqg","aWzlQ2N6qqg"))
    #recupInfosTweet('1384142929942368264')
    #recupListTweetCites("mbappe")
    #recupQuotedTweets('1385509857223192577')
    #recupListTweetCites('#ShangChi')
    #recupToutTweets(listFilms)
    get_database(recupToutTweets(listFilms))