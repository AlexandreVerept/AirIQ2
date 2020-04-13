import pandas as pd
import requests
from logger import Logger
from datetime import datetime
import numpy as np
import os

class pollutantCollector():    
    def collectRealtimePollutant(self,number_of_days=2):
        """
        get the air main pollutants of the last days
        
        Return: a panda dataframe with the data (and None if there is an error)
        """
        # download data
        try:
            URL = 'https://www.atmo-hdf.fr/acceder-aux-donnees/historique-des-indices-de-l-air.html?format=csv'
            r = requests.get(URL)
            filename = "export_{}.csv".format(datetime.now().strftime("%d%m%Y"))
            with open(filename,'wb') as output_file:
                output_file.write(r.content)
        except:
            Logger.log_error("Unable to import the data (pollutantCollector - collectRealtimePollutant)")
            try:
                os.remove(filename)
            except:
                None
            return(None)
           
        try:
            #data cleaning
            df = pd.read_csv(filename,header=0,delimiter=";",encoding="latin_1")
            os.remove(filename)
            interestingFeatures = ["Date","Dioxyde d'azote (NO2)","Ozone (O3)","Poussières PM10"]
            df = df[interestingFeatures]
            df.columns = ["date", "NO2", "O3", "PM10"]   
            
            df = df.drop(0) # drop today as the measures are made at the end of the day
            df = df.replace("/", np.nan)
            df = df.replace("N/D", np.nan)
            df = df.fillna(method='ffill')
                
            df = df.head(number_of_days)
        except:
            Logger.log_error("Error while shaping the data (pollutantCollector - collectRealtimePollutant)")
            try:
                os.remove(filename)
            except:
                None
            return(None)
        
            
        return(df)