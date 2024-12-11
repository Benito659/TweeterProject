from pymongo import MongoClient
import pymongo
from pymongo import MongoClient
import pandas as pd

uri = "mongodb://mongodbinstancenew:cvxgF0RwIc1SXw0vRbdcEyBp6BhmVriiKFBECUv4ToSbEI5tYinYXOJAW5Nv1PiYDNvsQyETsyT5otGwnJsHcg==@mongodbinstancenew.mongo.cosmos.azure.com:10255/?ssl=true&retrywrites=false&replicaSet=globaldb&maxIdleTimeMS=120000&appName=@mongodbinstancenew@"
client = pymongo.MongoClient(uri)
db_name = client["tweet_information_db"]
mycol = db_name["tweeteryoutubecollection"]

dftweeter = pd.DataFrame(columns = ['titre' , 'commentaire'])
for x in mycol.find():
    try :
        for commentaire in  x['tweetsHastag']:
            dftweeter=dftweeter.append({'titre' :x['title'], 'commentaire' : commentaire} , ignore_index=True)
    except:
        pass
print(dftweeter)