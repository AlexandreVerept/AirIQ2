import pandas as pd
import numpy as np
import requests
import json

class dataLinker():
    """
    this class allow us to send requests to the database
    """
    def __init__(self):
        try:
            with open('API_informations.json') as json_file:
                self.infos = json.load(json_file)
        except:
            print("Unable to load API_informations.json")
    
    def askForData(self):
        """
        ask for the informations needed to make a prediction
        """
        response = requests.get(self.infos["URL"]+"prediction")
        if(response.ok):
            data = json.loads(response.content)
        return(data)
        
    def postResult(self,prediction):
        """
        ask for the result of the prediction
        """
        print("TODO")