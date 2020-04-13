# DataCollector main program

import logging
from logger import Logger
from iq import iqCollector
from pollutant import pollutantCollector
from synop import synopCollector
from dataCollectorUtilities import dataLinker

logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)s %(message)s')

if __name__ == "__main__":
    
    # collect iq
    myIqCollector = iqCollector()
    iq = myIqCollector.collectRealtimeIQ(10)
    
    # collect pollutant
    myPollutantCollector = pollutantCollector()
    pollutant = myPollutantCollector.collectRealtimePollutant(10)
    
    # collect synop
    mySynopCollector = synopCollector()
    synop = mySynopCollector.collectRealtimeSynop(10)
    
    print(iq)
    print(pollutant)
    print(synop)
    
    # datalinker
    dl = dataLinker()
    dl.postIQ(iq)
    dl.postPollutant(pollutant)
    dl.postSynop(synop)
    