# Main program of the Backend flask API

from flask import Flask
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

@app.route('/realtimepredictions',methods=['POST'])
def realTimePredictions():
    """
    collect predictions of the index quality from the script python dedicated to this task
    """
    dbc = dataBaseConnector()
    return(dbc.getRealTimePredictions())
    
@app.route('/informationsdatacollector', methods=['POST'])
def informationsDataCollector():
    """
    collect all datas to put into the database
    """
    dbc = dataBaseConnector()
    return(dbc.getInformationsDataCollector())
    
@app.route('/prediction', methods = ['GET'])
def prediction():
    """
    receive the dictionary and fill in the database
    """
    dbc = dataBaseConnector()
    return(dbc.getInformationsDataCollector())

if __name__ == "__main__":
    app.run()