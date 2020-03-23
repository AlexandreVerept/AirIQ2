# DataCollector main program

import logging
from logger import Logger
from iq import iqCollector
from pollutant import pollutantCollector
from synop import synopCollector
import pandas as pd

import requests

logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)s %(message)s')

if __name__ == "__main__":
    
    # collect iq from the last 2 days and print it for now:
    myIqCollector = iqCollector()
    iq = myIqCollector.collectRealtimeIQ()
    
    myPollutantCollector = pollutantCollector()
    pollutant = myPollutantCollector.collectRealtimePollutant()
    
    mySynopCollector = synopCollector()
    synop = mySynopCollector.collectRealtimeSynop()
    
    print(iq)
    print(pollutant)
    print(synop)
    
    # send to the API
    url = 'http://127.0.0.1:5000/test'
    r = requests.post(url, json=iq.to_dict())
    print(r.status_code)