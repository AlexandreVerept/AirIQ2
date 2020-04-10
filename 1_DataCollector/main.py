# DataCollector main program

import logging
from logger import Logger
from iq import iqCollector
from pollutant import pollutantCollector
from synop import synopCollector
import pandas as pd
from dataCollectorUtilities import dataLinker

logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)s %(message)s')

if __name__ == "__main__":
    
    # collect iq
    myIqCollector = iqCollector()
    iq = myIqCollector.collectRealtimeIQ(10)
    
    #myPollutantCollector = pollutantCollector()
    #pollutant = myPollutantCollector.collectRealtimePollutant(3)
    
    mySynopCollector = synopCollector()
    synop = mySynopCollector.collectRealtimeSynop(10)
    
    print(iq)
    #print(pollutant)
    print(synop)
    
    dl = dataLinker()
    dl.postIQ(iq)
    #dl.postPolutant(pollutant)
    dl.postSynop(synop)
    