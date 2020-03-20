import pandas as pd
from logger import Logger
from datetime import datetime, timedelta

class synopCollector():
    def collectRealtimeSynop(self,number_of_days=2):
        """
        get the main weather informations of the last days
        
        Return: a panda dataframe with the data (and None if there is an error)
        """
        if number_of_days>15:
            Logger.log_error("Error, number of days must be inferior or equal to 15 (synopCollector - collectRealtimeSynop)")
            raise Exception('Number of days must be inferior or equal to 15')                
        
        dataframes = []
        for day in range(number_of_days):
            try:
                dateRequest = datetime.strftime(datetime.now() - timedelta(day), '%Y%m%d')
                CSV_URL = "https://donneespubliques.meteofrance.fr/donnees_libres/Txt/Synop/synop.{}09.csv".format(str(dateRequest))
                df = pd.read_csv(CSV_URL, delimiter=';')
            except:
                Logger.log_error("Unable to retrive the Meteo France Synop CSV file (synopCollector - collectRealtimeSynop)")
            finally:
                
                # data cleaning: for more explanations, go to "AirIQ2\0_ResearchWork\3_CleanDatasetSynop"
                try:
                    df = df[df["numer_sta"] == 7015]
                    interestingFeatures = ["date","pres","dd","ff"]
                    df = df[interestingFeatures]
                    df.columns = ["date", "pressure","wind_direction","wind_force"]
            
                    df["pressure"] = df["pressure"].astype(int)
                    df["wind_direction"] = df["wind_direction"].astype(int)
                    df["wind_force"] = df["wind_force"].astype(float)
                    df["date"] = pd.to_datetime(df["date"].astype(str), format='%Y%m%d%H%M%S').astype(str).apply(lambda x: x[0:10])
                
                    dataframes.append(df)
                except:
                    Logger.log_error("Error while processing the CSV data (synopCollector - collectRealtimeSynop)")
        try:
            return(pd.concat(dataframes))
        except:
            Logger.log_error("Error concatenate (synopCollector - collectRealtimeSynop)")
            return(None)