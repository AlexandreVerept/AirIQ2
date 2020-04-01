# This script is used for the realtime prediction

from prediction import predictionMaker
from dataUtilities import dataLinker
import logging
import pandas as pd

logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)s %(message)s')

if __name__ == '__main__':
    
    # create our classes
    pm = predictionMaker()
    dl = dataLinker()
    
    # ask for the data needed
    data = dl.askForData()    
    
    # return the prediction
    #predict = pm.makePrediction(data)
    
    # post the results to the API
    #dl.postResult(predict)