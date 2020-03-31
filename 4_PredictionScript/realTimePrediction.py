# This script is used for the realtime prediction

from prediction import predictionMaker
from dataUtilities import dataLinker

if __name__ == '__main__':
    
    # create our classes
    pm = predictionMaker()
    dl = dataLinker()
    
    # ask for the data needed
    data = dl.askForData()
    
    # return the prediction
    predict = pm.makePrediction(data)
    
    # post the results to the API
    dl.postResult(predict)