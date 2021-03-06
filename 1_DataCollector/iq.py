import pandas as pd
import urllib.request
import json
from logger import Logger
from datetime import datetime
    
class iqCollector():    
    def collectRealtimeIQ(self,number_of_days=2):
        """
        get the air index quality of the last days
        
        Return: a panda dataframe with the data (and None if there is an error)
        """
        #make a request:
        try:
            request = "https://opendata.lillemetropole.fr/api/records/1.0/search/?dataset=indice-qualite-de-lair&sort=date_ech&rows={}".format(number_of_days)
            with urllib.request.urlopen(request) as jsonfile:
                data = json.loads(jsonfile.read().decode())
        except:
            Logger.log_error("Unable to connect to the MEL API (iqCollector - collectRealtimeIQ)")
            return(None)
            
        #treat the response:
        try:
            listeDesRecords = data['records']
            listeDesFields = []
            for r in listeDesRecords: # we get each field of the answer
                listeDesFields.append(r['fields']) 
            dico = []
            for k in listeDesFields:
                #dico.append({'date' : datetime.fromtimestamp(int(k['date_ech'])).strftime('%Y-%m-%d'),'value' : k['valeur']})
                dico.append({'date' : k['date_ech'][0:10],'value' : k['valeur']})
            df = pd.DataFrame(dico)
        except:
            Logger.log_error("Error while processing the MEL data from the API (iqCollector - collectRealtimeIQ)")
            return(None)  
            
        return(df)