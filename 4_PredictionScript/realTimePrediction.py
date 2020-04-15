# This script is used for the realtime prediction

from prediction import predictionMaker
from dataUtilities import dataLinker
import logging
from logger import Logger
import schedule
import time

logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)s %(message)s')

THRESHOLD = 5

def call_script():
    # create our classes
    pm = predictionMaker()
    dl = dataLinker()
    
    # ask for the data needed
    success = False
    attempt = 0
    while not success and attempt < THRESHOLD:
        try:
            x_pred,dayConsidered = dl.askForData(32)
            success = True
        except:
            attempt += 1
            time.sleep(30 * attempt)
            if attempt >= THRESHOLD:
                Logger.log_error("To many errors while asking for data")
                
    if success:
        # return the prediction
        success = False
        attempt = 0
        while not success and attempt < THRESHOLD:
            try:
                y_pred = pm.makePrediction(x_pred)
                success = True
            except:
                attempt += 1
                time.sleep(30 * attempt)
                if attempt >= THRESHOLD:
                    Logger.log_error("To many errors while making the prediction")
                    
        # post the results to the API
        if success:
            # return the prediction
            success = False
            attempt = 0
            while not success and attempt < THRESHOLD:
                try:
                    dl.postResult(y_pred,dayConsidered)
                    success = True
                except:
                    attempt += 1
                    time.sleep(30 * attempt)
                    if attempt >= THRESHOLD:
                        Logger.log_error("To many errors while making the prediction")
        
        Logger.log_info("Prediction sucessful")


if __name__ == '__main__':
    # Schedule the script to launch everyday at 12:00
    schedule.every().day.at('11:45').do(call_script)
    #schedule.every(1).minutes.do(call_script)

    # Boucle infinie afin de pouvoir appeler la fonction au moment predefini 
    while True:
        schedule.run_pending()
        time.sleep(60)