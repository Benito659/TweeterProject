from pymongo import MongoClient
import pymongo
from pymongo import MongoClient


from flask import Flask, jsonify, request 

app = Flask(__name__) 

@app.route('/data/', methods = ['GET', 'POST']) 
def dataRestit(): 
    if(request.method == 'GET'): 
        client = MongoClient('localhost', port=8084)
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
