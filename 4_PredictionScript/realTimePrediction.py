# This script is used for the realtime prediction

from prediction import predictionMaker
from dataUtilities import dataLinker
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)s %(message)s')

if __name__ == '__main__':
    # create our classes
    pm = predictionMaker()
    dl = dataLinker()
    
    # ask for the data needed
    x_pred,dayConsidered = dl.askForData(32)
    
    # return the prediction
    y_pred = pm.makePrediction(x_pred)
    
    # post the results to the API
    dl.postResult(y_pred,dayConsidered)