from pymongo import MongoClient
uri = "mongodb://mongodbinstancenew:cvxgF0RwIc1SXw0vRbdcEyBp6BhmVriiKFBECUv4ToSbEI5tYinYXOJAW5Nv1PiYDNvsQyETsyT5otGwnJsHcg==@mongodbinstancenew.mongo.cosmos.azure.com:10255/?ssl=true&retrywrites=false&replicaSet=globaldb&maxIdleTimeMS=120000&appName=@mongodbinstancenew@"
client = MongoClient(uri)

# Create a new collection
db_name = client["tweet_information_db"]
mycol = db_name["tweeteryoutubecollection"]

x = mycol.delete_many({})

print(x.deleted_count, " documents deleted.")