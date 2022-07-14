from pymongo import MongoClient
import pymongo
from pymongo import MongoClient


from flask import Flask, jsonify, request 

app = Flask(__name__) 

@app.route('/data/', methods = ['GET']) 
def dataRestit(): 
    if(request.method == 'GET'): 
        uri = "mongodb://mongodbinstancenew:cvxgF0RwIc1SXw0vRbdcEyBp6BhmVriiKFBECUv4ToSbEI5tYinYXOJAW5Nv1PiYDNvsQyETsyT5otGwnJsHcg==@mongodbinstancenew.mongo.cosmos.azure.com:10255/?ssl=true&retrywrites=false&replicaSet=globaldb&maxIdleTimeMS=120000&appName=@mongodbinstancenew@"
        client = pymongo.MongoClient(uri)
        db_name = client["tweet_information_db"]
        mycol = db_name["tweeteryoutubecollection"]
        listDB=[]
        for x in mycol.find():
            x.pop('_id')
            try:
                x["tweetsResponse"] =[str(item["text"]) for item in x["tweetsResponse"]]
            except:
                pass
            try:
                comentaireYoutubeList=[str(item["Comment Text:"]) for item in x["youtubeResult"]["Commentaires"]]
                likeYoutubeParCommentaireList=[int(item["Likes on Comment:"]) for item in x["youtubeResult"]["Commentaires"]]
                x.update({'commentaireYoutube':comentaireYoutubeList})
                x.update({'likeYoutubeParCommentaire':likeYoutubeParCommentaireList})
            except:
                pass

            listDB.append(x)
        return jsonify({'data': listDB}) 


@app.route('/model/', methods = ['GET']) 
def modelCall(): 
    return jsonify({'data': num**2}) 

@app.route('/') 
def disp(): 
    return """<iframe title="latest" width="1140" height="541.25" src="https://app.powerbi.com/reportEmbed?reportId=e05d2515-0e68-47d4-8dee-50b5a4e0f382&autoAuth=true&ctid=987b6351-7e5c-42d9-8e61-3830e896b75e&config=eyJjbHVzdGVyVXJsIjoiaHR0cHM6Ly93YWJpLW5vcnRoLWV1cm9wZS1yZWRpcmVjdC5hbmFseXNpcy53aW5kb3dzLm5ldC8ifQ%3D%3D" frameborder="0" allowFullScreen="true"></iframe>"""


if __name__ == '__main__': 
    app.run(debug = True) 
