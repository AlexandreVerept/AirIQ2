# DataCollector main program

import logging
from logger import Logger
from iq import iqCollector
from pollutant import pollutantCollector
from synop import synopCollector
from dataCollectorUtilities import dataLinker
import schedule
import time

logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)s %(message)s')

THRESHOLD = 5
DAYS = 5

def call_script():
    # collect iq
    myIqCollector = iqCollector()
    
    success = False
    attempt = 0
    while not success and attempt < THRESHOLD:
        try:
            iq = myIqCollector.collectRealtimeIQ(DAYS)
            if iq is not None:
                success = True
            else:
                attempt += 1
                time.sleep(30 * attempt)
                if attempt >= THRESHOLD:
                    raise ValueError()
        except:
            attempt += 1
            time.sleep(30 * attempt)
            if attempt >= THRESHOLD:
                Logger.log_error("To many errors while asking for IQ")

    
    # collect pollutant
    if success:
        myPollutantCollector = pollutantCollector()
        # return the prediction
        success = False
        attempt = 0
        while not success and attempt < THRESHOLD:
            try:
                pollutant = myPollutantCollector.collectRealtimePollutant(DAYS)
                if pollutant is not None:
                    success = True
                else:
                    attempt += 1
                    time.sleep(30 * attempt)
                    if attempt >= THRESHOLD:
                        raise ValueError()
            except:
                attempt += 1
                time.sleep(30 * attempt)
                if attempt >= THRESHOLD:
                    Logger.log_error("To many errors while asking for Pollutant")
                    
        # collect synop
        mySynopCollector = synopCollector()
        if success:
            success = False
            attempt = 0
            while not success and attempt < THRESHOLD:
                try:
                    synop = mySynopCollector.collectRealtimeSynop(DAYS)
                    if synop is not None:
                        success = True
                    else:
                        attempt += 1
                        time.sleep(30 * attempt)
                        if attempt >= THRESHOLD:
                            raise ValueError()
                except:
                    attempt += 1
                    time.sleep(30 * attempt)
                    if attempt >= THRESHOLD:
                        Logger.log_error("To many errors while asking for Synop")
                        
    if success:
        Logger.log_info("Import data sucessfully")
        
        # datalinker
        dl = dataLinker()            
        if success:
            success = False
            attempt = 0
            while not success and attempt < THRESHOLD:
                try:
                    dl.postIQ(iq)
                    dl.postPollutant(pollutant)
                    dl.postSynop(synop)
                    success = True
                except:
                    attempt += 1
                    time.sleep(30 * attempt)
                    if attempt >= THRESHOLD:
                        Logger.log_error("To many errors while filling the database")
    if success:
        Logger.log_info("Export data sucessfully")
    
if __name__ == '__main__':
    # Schedule the script to launch everyday at 12:01
    schedule.every().day.at('11:00').do(call_script)
    
    call_script()

    while True:
        schedule.run_pending()
        time.sleep(60)
    