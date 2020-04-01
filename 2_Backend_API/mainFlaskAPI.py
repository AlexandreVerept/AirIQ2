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
    return("Welcome to our backend API. You can find the documentation here: https://github.com/AlexandreVerept/AirIQ2/blob/master/5_Frontend_API/README.md")
    
    
@app.route('/test',methods=['POST'])
def test():
    """
    test for connection json
    """
    r = str(request.get_json())
    print(r)
    return(r)
    

@app.route('/prediction', methods = ['GET'])
def getPredictionInformations():
    """
    send informations needed to make the prediction
    """
    dbc = dataBaseConnector()
    return(jsonify(dbc.getInformationsDataCollector()))
    
    
@app.route('/realtimepredictions',methods=['POST'])
def postRealTimePredictions():
    """
    collect predictions of the index quality from the script python dedicated to this task and put it in the DB
    """
    dbc = dataBaseConnector()
    return(dbc.postRealTimePredictions(request.get_json()))

    
@app.route('/infodatacollector/<typeOfValue>', methods=['POST'])
def postInformationsDataCollector(typeOfValue):
    """
    collect all datas from the data collector to put into the DB
    """
    dbc = dataBaseConnector()
    return(dbc.postInformationsDataCollector(request.get_json(),typeOfValue))


if __name__ == "__main__":
    app.run()