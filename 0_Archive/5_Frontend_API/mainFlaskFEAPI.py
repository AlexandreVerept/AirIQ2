# Main program of the Frontend flask API

from flask import Flask, jsonify
import logging
from dataBaseUtilitiesFE import dataBaseConnector

logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)s %(message)s')

app = Flask(__name__)

@app.route('/',methods=['GET'])
def welcome():
    """
    Welcome the user and give him a link to the documentation/github
    """
    return("Welcome to our frontend API, you can find documentation here: https://github.com/AlexandreVerept/AirIQ2/blob/master/2_Backend_API/README.md")


@app.route('/allpredictions',methods=['GET'])
def allPredictions():
    """
    retrieve all the predictions from te database
    """
    dbc = dataBaseConnector()
    return(jsonify(dbc.getAllPredictions()))
    
    
@app.route('/getprediction', defaults={'numberOfDays': 0}, methods = ['GET'])
@app.route('/getprediction/<numberOfDays>', methods = ['GET'])
def getPredictions(numberOfDays):
    """
    retrieve all the predictions from te database for the last x days
    """
    dbc = dataBaseConnector()
    return(jsonify(dbc.getLastsPredictions(numberOfDays)))
    

if __name__ == "__main__":
    app.run()