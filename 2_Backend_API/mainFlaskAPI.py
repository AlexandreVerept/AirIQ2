# Main program of the Backend flask API

from flask import Flask, jsonify, request
import logging
from dataBaseUtilities import dataBaseConnector

logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)s %(message)s')

app = Flask(__name__)


@app.route('/',methods=['GET'])
def welcome():
    """
    Welcome the user and give him a link to the documentation/github
    """
    return("Welcome to our API")
    

@app.route('/prediction', methods = ['GET'])
def getPredictionInformations():
    """
    send informations needed to make the prediction
    """
    dbc = dataBaseConnector()
    return (jsonify(dbc.getInformationsDataCollector()))
    
    
    
    
    
    
    
    
    
    
    


@app.route('/realtimepredictions',methods=['POST'])
def postRealTimePredictions():
    """
    collect predictions of the index quality from the script python dedicated to this task and put it in the DB
    """
    dbc = dataBaseConnector()
    return(dbc.postRealTimePredictions())
    
    
@app.route('/informationsdatacollector', methods=['POST'])
def postInformationsDataCollector():
    """
    collect all datas from the data collector to put into the DB
    """
    dbc = dataBaseConnector()
    return(dbc.postInformationsDataCollector())
    
    
    

if __name__ == "__main__":
    app.run()