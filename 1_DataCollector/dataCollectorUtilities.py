import pandas as pd
import numpy as np
import requests
import json
from logger import Logger

class dataLinker():
    """
    this class allow us to send the collected data to the database
    """
    def __init__(self):
        try:
            with open('API_informations.json') as json_file: #TODO change test to cloud
                self.infos = json.load(json_file)
        except:
            Logger.log_error("Unable to load API_informations.json")
            
            
    def postIQ(self,iq):
        """
        Post the coolected IQ in the API
        """
        return(self.postData(iq.to_dict(),"iq"))
    
    def postPollutant(self,pollutants):
        """
        Post the coolected polutants in the API
        """
        return(self.postData(pollutants.to_dict(),"pollutant"))
    
    def postSynop(self,synop):
        """
        Post the coolected IQ in the API
        """
        return(self.postData(synop.to_dict(),"synop"))
            
    def postData(self,data,method):
        """
        Post the coolected data in the API
        """
        if not data:
            return(None)       
        response = requests.post(url = self.infos["URL"]+"infodatacollector/{}".format(method), json = data)
        if not response.ok:
            Logger.log_error("Unable to POST the data")
        return(True)