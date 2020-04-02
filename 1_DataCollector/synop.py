import pandas as pd
from logger import Logger
from datetime import datetime, timedelta
import os
import requests
import gzip

class synopCollector():
    def collectRealtimeSynop(self,number_of_days=2):
        """
        get the main weather informations of the last days
        
        Return: a panda dataframe with the data (and None if there is an error)
        """
        
        # the site stock the informations by mont, so we have to download all the months we need
        URL = 'https://donneespubliques.meteofrance.fr/donnees_libres/Txt/Synop/Archive/'
        dataframes = []
        listOfMonthAlreadyMade = []
        try:
            for day in range(number_of_days):
                dateDelta = datetime.strftime(datetime.now() - timedelta(day), '%Y%m')
                if not dateDelta in listOfMonthAlreadyMade:
                    listOfMonthAlreadyMade.append(dateDelta)
                    filename = "synop.{}.csv.gz".format(dateDelta)
                    r = requests.get(URL+"/"+filename)
                    with gzip.open(filename,'wb') as output_file:
                        output_file.write(r.content)
            
                    df = pd.read_csv(filename, header=0, delimiter=';')
                    
                    # a bit of cleaning
                    df = df[df["numer_sta"] == 7015]
                    interestingFeatures = ["date","pres","dd","ff","u","t"]
                    df = df[interestingFeatures]
                    df.columns = ["date", "pressure","wind_direction","wind_force","humidity","temperature"]
                    df["pressure"] = df["pressure"].astype(int)
                    df["wind_direction"] = df["wind_direction"].astype(int)
                    df["wind_force"] = df["wind_force"].astype(float)
                    df["humidity"] = df["humidity"].astype(int)
                    df["temperature"] = df["temperature"].astype(float)
                    df["date"] = pd.to_datetime(df["date"], format='%Y%m%d%H%M%S')
                    dataframes.append(df)
                    os.remove(filename)
        except:
            Logger.log_error("Unable to retrive the Meteo France Synop CSV file (synopCollector - collectRealtimeSynop)")
            try: # try to clear the last file just in case
                os.remove(filename)
            except:
                None
        #then we concatenate the result
        try:
            df = pd.concat(dataframes)
        except:
            Logger.log_error("Error concatenate (synopCollector - collectRealtimeSynop)")
            return(None)
        
        #finally we select the days we wanted:
        try:
            df = df.loc[(df['date'] > datetime.now() - timedelta(number_of_days)) & (df['date'] <= datetime.now())].sort_values(by=['date'], ascending=False)
            df['date'] = df['date'].astype(str)
            return(df)
        except:
            Logger.log_error("Error selecting days (synopCollector - collectRealtimeSynop)")
            return(None)