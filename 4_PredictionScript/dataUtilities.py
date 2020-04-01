import pandas as pd
import numpy as np
import requests
import json
from logger import Logger


class dataLinker():
    """
    this class allow us to send requests to the database
    """
    def __init__(self):
        try:
            with open('API_informations.json') as json_file:
                self.infos = json.load(json_file)
        except:
            Logger.log_error("Unable to load API_informations.json")
            
    
    def askForData(self):
        """
        ask for the informations needed to make a prediction
        return a tuple of dataframes
        """
        try:
            response = requests.get(self.infos["URL"]+"prediction")
            if response.ok:
                data = json.loads(response.content)
        except:
            Logger.log_error("Unable to ask the API for the content of prediction")
        
        # convert to dataframe
        data = [pd.DataFrame.from_dict(data[0]),pd.DataFrame.from_dict(data[1])]
        #TODO shape the data:
        
            
        return(None)
        
        
    def postResult(self,prediction):
        """
        Post the result of the prediction in the API
        """
        if not prediction:
            return(None)
            
        response = requests.post(url = self.infos["URL"]+"realtimepredictions", data = prediction)
        if not response.ok:
            Logger.log_error("Unable to POST the prediction")