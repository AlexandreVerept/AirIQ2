# DataCollector main program

import logging
from logger import Logger
from iq import iqCollector
from pollutant import pollutantCollector
from synop import synopCollector
import pandas as pd
from dataUtilities import dataLinker

logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)s %(message)s')

if __name__ == "__main__":
    
    # collect iq from the last 2 days and print it for now:
    myIqCollector = iqCollector()
    iq = myIqCollector.collectRealtimeIQ(1000)
    
    #myPollutantCollector = pollutantCollector()
    #pollutant = myPollutantCollector.collectRealtimePollutant(3)
    
    mySynopCollector = synopCollector()
    synop = mySynopCollector.collectRealtimeSynop(40000)
    
    print(iq)
    #print(pollutant)
    print(synop)
    
    dl = dataLinker()
    dl.postIQ(iq)
    #dl.postPolutant(pollutant)
    dl.postSynop(synop)
    