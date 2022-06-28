from pymongo import MongoClient
import pymongo
from pymongo import MongoClient


from flask import Flask, jsonify, request 

app = Flask(__name__) 

@app.route('/data/', methods = ['GET', 'POST']) 
def dataRestit(): 
    if(request.method == 'GET'): 
        uri = "mongodb://mongodbinstancenew:cvxgF0RwIc1SXw0vRbdcEyBp6BhmVriiKFBECUv4ToSbEI5tYinYXOJAW5Nv1PiYDNvsQyETsyT5otGwnJsHcg==@mongodbinstancenew.mongo.cosmos.azure.com:10255/?ssl=true&retrywrites=false&replicaSet=globaldb&maxIdleTimeMS=120000&appName=@mongodbinstancenew@"
        client = pymongo.MongoClient(uri)
        db_name = client["tweet_information_db"]
        mycol = db_name["tweeteryoutubecollection"]
        listDB=[]
        for x in mycol.find():
            x.pop('_id')
            listDB.append(x)
        return jsonify({'data': listDB}) 


@app.route('/model/', methods = ['GET']) 
def disp(): 
    return jsonify({'data': num**2}) 




if __name__ == '__main__': 
    app.run(debug = True) 
