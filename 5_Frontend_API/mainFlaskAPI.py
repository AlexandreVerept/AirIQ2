# Main program of the Frontend flask API

from flask import Flask, jsonify
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

@app.route('/allpredictions',methods=['GET'])
def allPredictions():
    """
    retrieve all the predictions from te database
    """
    dbc = dataBaseConnector()
    return(jsonify(dbc.getAllPredictions()))
    

if __name__ == "__main__":
    app.run()