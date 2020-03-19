# DataCollector main program

import time
import logging
from logger import Logger
from iq import iqCollector
from pollutant import pollutantCollector

logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)s %(message)s')

if __name__ == "__main__":
    
    # collect iq from the last 2 days and print it for now:
    myIqCollector = iqCollector()
    print(myIqCollector.collectRealtimeIQ())
    
    myPollutantCollector = pollutantCollector()
    print(myPollutantCollector.collectRealtimePollutant())