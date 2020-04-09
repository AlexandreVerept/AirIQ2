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
    return("Welcome to our API. You can find the documentation here: https://github.com/AlexandreVerept/AirIQ2/blob/master/")
    
    
@app.route('/test',methods=['POST'])
def test():
    """
    test for connection json
    """
    r = str(request.get_json())
    print(r)
    return(r)
    
@app.route('/prediction', defaults={'numberOfDays': 2}, methods = ['GET'])
@app.route('/prediction/<numberOfDays>', methods = ['GET'])
def getPredictionInformations(numberOfDays):
    """
    send informations needed to make the prediction
    """
    dbc = dataBaseConnector()
    return(jsonify(dbc.getDataNeededPrediction(numberOfDays)))
    
    
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