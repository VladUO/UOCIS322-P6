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
        app.logger.debug(format)  # checking format
        
        # pulling out the k value and checking it
        k = request.args.get('top', default = 0, type=int)
        app.logger.debug(k)

        # pulling out unnecessary items from the list and clearning the list    
        data = list(db.database.find({}, {'_id': 0, 'BrevetDistance':0, 'StartTime':0, 'Location': 0, 'Km':0, 'Miles':0}))
        data.remove({})
        # app.logger.debug("DATA FROM MONGODB", data)
        
        # depending on the selected output format, sending the resulting list to the appropriate support function
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
        app.logger.debug(format) # checking format 
        
        # pulling out the k value and checking it
        k = request.args.get('top', default = 0, type=int)
        app.logger.debug(k)

        # pulling out unnecessary items from the list and clearning the list  
        data = list(db.database.find({}, {'_id': 0, 'BrevetDistance':0, 'StartTime':0, 'Location': 0, 'Km':0, 'Miles':0, 'Close':0}))
        data.remove({})
        # app.logger.debug("DATA FROM MONGODB", data)

        # depending on the selected output format, sending the resulting list to the appropriate support function
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
        app.logger.debug(format) # checking format    

        # pulling out the k value and checking it
        k = request.args.get('top', default = 0, type=int)
        app.logger.debug(k)

        # pulling out unnecessary items from the list and clearning the list  
        data = list(db.database.find({}, {'_id': 0, 'BrevetDistance':0, 'StartTime':0, 'Location': 0, 'Km':0, 'Miles':0, 'Open':0}))
        data.remove({})
        # app.logger.debug("DATA FROM MONGODB", data)

        # depending on the selected output format, sending the resulting list to the appropriate support function
        if format == "Json":
            return toJson(k, data)
        elif format == "CSV":    
            return toCSV(k, data)
        else:
            return "ERROR" 

# support function for converting to JSON format
def toJson(k, data):
    # create a new list
    newlist = []
    # if we have a k value and its less than the total number of rows
    # loop through data and append each row from data to the list
    # then jsonify the list and return it
    if k > 0 and k <= len(data):
        for i in range(0, k):
            newlist.append(dict(data[i]))
            app.logger.debug("LIST", newlist)
        return jsonify(newlist)
    
    # otherwise just jsonify the original list and return that
    else:
        return jsonify(data)

# support function for converting to CSV format
def toCSV(k, data):
    # create a new list
    newlist = [] 
    # if we have a k value and its less than the total number of rows
    # loop through data and append each row from data to the list
    # then turn that list into a dataframe, convert to CSV using to_csv and return
    if k > 0 and k <= len(data):
        for i in range(0, k):
            newlist.append(dict(data[i]))
            app.logger.debug("LIST", newlist)
        df = pd.DataFrame(newlist)
               
        return df.to_csv(index=False)

    # otherwise just convert the original list to dataframe, then to CSV and return
    else:
        df = pd.DataFrame(data)
        
        return df.to_csv(index=False)


# # Create routes
# # Another way, without decorators
api.add_resource(listAll, '/listAll/<string:format>')
api.add_resource(listOpenOnly, '/listOpenOnly/<string:format>')
api.add_resource(listCloseOnly, '/listCloseOnly/<string:format>')

# Run the application
if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
