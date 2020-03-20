import pandas as pd
import urllib.request
import json
from logger import Logger

class pollutantCollector():    
    def collectRealtimePollutant(self,number_of_days=2):
        """
        get the air main pollutants of the last days
        
        Return: a panda dataframe with the data (and None if there is an error)
        """
        #make a request:
        try:
            request = "https://opendata.lillemetropole.fr/api/records/1.0/search/?dataset=mesures-journalieres-des-principaux-polluants&rows={}&sort=date_fin&refine.nom_com=Lille&refine.nom_station=Lille+Fives".format(number_of_days*4)
            with urllib.request.urlopen(request) as jsonfile:
                data = json.loads(jsonfile.read().decode())
        except:
            Logger.log_error("Unable to connect to the MEL API (pollutantCollector - collectRealtimePollutant)")
            return(None)
            
        #treat the response:
        try:
            listeDesRecords = data['records']
            listeDesFields = []
            for r in listeDesRecords: # we get each field of the answer
                listeDesFields.append(r['fields']) 
            #print(listeDesFields)
            dico = []
            for k in listeDesFields:
                try:
                    dico.append({'date' : k['date_fin'][0:10],'value' : k['valeur'],'name_poll' : k['nom_poll'],'city' : k['nom_com']})
                except: #sometimes the values are not defined
                    dico.append({'date' : k['date_fin'][0:10],'value' : None,'name_poll' : k['nom_poll'],'city' : k['nom_com']})
            df = pd.DataFrame(dico)
        except:
            Logger.log_error("Error while processing the MEL data from the API (pollutantCollector - collectRealtimePollutant)")
            return(None)  
        
        # if some values are missing we fill in the gaps:
        if df.isnull().values.any():
            nan_rows = df[df['value'].isnull()]
            for pollutant in nan_rows.name_poll.unique():
                df[df['name_poll'] == pollutant] = df[df['name_poll'] == pollutant].fillna(method='ffill')
            
        return(df)