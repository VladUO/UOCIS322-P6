# Streaming Service

import os
from os import O_RDONLY
from flask import Flask, render_template, request, jsonify
from flask_restful import Resource, Api
import json
import pandas as pd

from pymongo import MongoClient

app = Flask(__name__)
api = Api(app)

# importing our database 
client = MongoClient('mongodb://' + os.environ['MONGODB_HOSTNAME'], 27017)
db = client.database

# class for listing all times
class listAll(Resource):
    def get(self, format):
        app.logger.debug("ENTERED listAll in API")
        app.logger.debug(format)  

        k = request.args.get('top', default = 0, type=int)
        app.logger.debug(k)


        data = list(db.database.find({}, {'_id': 0, 'BrevetDistance':0, 'StartTime':0, 'Location': 0, 'Km':0, 'Miles':0}))
        data.remove({})
        # app.logger.debug("DATA FROM MONGODB", data)
        
        if format == "Json":
            return toJson(k, data)
        elif format == "CSV":    
            return toCSV(k, data)
        else:
            return "ERROR"     

# class for listing open times only
class listOpenOnly(Resource):
    def get(self, format):
        app.logger.debug("ENTERED listOpenOnly in API")  
        app.logger.debug(format)  
        
        k = request.args.get('top', default = 0, type=int)
        app.logger.debug(k)

        data = list(db.database.find({}, {'_id': 0, 'BrevetDistance':0, 'StartTime':0, 'Location': 0, 'Km':0, 'Miles':0, 'Close':0}))
        data.remove({})
        # app.logger.debug("DATA FROM MONGODB", data)

        if format == "Json":
            return toJson(k, data)
        elif format == "CSV":    
            return toCSV(k, data)
        else:
            return "ERROR" 

# class for listing close times only
class listCloseOnly(Resource):
    def get(self, format):
        app.logger.debug("ENTERED listCloseOnly in API") 
        app.logger.debug(format)     

        k = request.args.get('top', default = 0, type=int)
        app.logger.debug(k)

        data = list(db.database.find({}, {'_id': 0, 'BrevetDistance':0, 'StartTime':0, 'Location': 0, 'Km':0, 'Miles':0, 'Open':0}))
        data.remove({})
        # app.logger.debug("DATA FROM MONGODB", data)

        if format == "Json":
            return toJson(k, data)
        elif format == "CSV":    
            return toCSV(k, data)
        else:
            return "ERROR" 

def toJson(k, data):
    newlist = []
    if k > 0 and k <= len(data):
        for i in range(0, k):
            newlist.append(dict(data[i]))
            app.logger.debug("LIST", newlist)
        return jsonify(newlist)
    
    else:
        return jsonify(data)


def toCSV(k, data):
    newlist = [] 
    # app.logger.debug("DATA DATA DATA",data)

    if k > 0 and k <= len(data):
        for i in range(0, k):
            newlist.append(dict(data[i]))
            app.logger.debug("LIST", newlist)
        df = pd.DataFrame(newlist)
        app.logger.debug("DATAFRAME", df)
        
        return df.to_csv(index=False)

    else:
        df = pd.DataFrame(data)
        # app.logger.debug("DATAFRAME", df)

        return df.to_csv(index=False)


# # Create routes
# # Another way, without decorators
api.add_resource(listAll, '/listAll/<string:format>')
api.add_resource(listOpenOnly, '/listOpenOnly/<string:format>')
api.add_resource(listCloseOnly, '/listCloseOnly/<string:format>')

# Run the application
if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
