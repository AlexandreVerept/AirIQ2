import pandas as pd
import numpy as np
import requests
import json
from logger import Logger
from datetime import datetime

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
            
    
    def askForData(self,nbNeededObservation=32):
        """
        ask for the informations needed to make a prediction
        
        return the data frame for the prediction and the dayConsidered (to know which 
        day we consider as we can only do a prediction at 12:00, even if we are 
        the next day at 9:00, the prediction will be dated as the previous day)
        """
        numberOfDays = int(nbNeededObservation/8)+1 # the theorical number of days we need + 1 day for safety
        try:
            response = requests.get(self.infos["URL"]+"prediction/{}".format(numberOfDays))
            if response.ok:
                data = response.json()
        except:
            Logger.log_error("Unable to ask the API for the content of prediction")
            return(None)
        
        try:
            # convert to dataframe
            dfiq,dfsynop,dfp = pd.DataFrame.from_dict(data[0]),pd.DataFrame.from_dict(data[1]),pd.DataFrame.from_dict(data[2])
            
            
            # Shape the data:
            # 1 - mix the datasets: 
            #(please see "MixDatasets.ipynb" in the data cleaning section of our researchs for more information)
            dfiq['date'] = pd.to_datetime(dfiq['date'],utc=True)
            dfsynop['date'] = pd.to_datetime(dfsynop['date'],utc=True)
            dfp['date'] = pd.to_datetime(dfp['date'],utc=True)
            
            # make sure we have the today data for the pollutant with ffil:     
            dfp = dfp.append({"date": datetime.now().strftime("%Y-%m-%d")+" 00:00:00+00:00"},ignore_index=True)
            dfp['date'] = pd.to_datetime(dfp['date'],utc=True)
            dfp = dfp.drop_duplicates()
            dfp = dfp.sort_values(by="date")
            dfp = dfp.fillna(method = "ffill")            
                        
            def getDay(row):
                return(row["date"].date())

            dfsynop["day"] = dfsynop.apply(lambda row: getDay(row), axis=1)
            dfiq["day"] = dfiq.apply(lambda row: getDay(row), axis=1)
            dfp["day"] = dfp.apply(lambda row: getDay(row), axis=1)
            
            dfp = dfp.drop(columns="date")
        
            df = pd.merge(dfiq, dfsynop, how='inner', on="day")
            df = pd.merge(df,dfp, how='inner', on="day")
            df = df.drop(columns=["date_x","day"])
            df = df.rename(columns={"date_y":"date", "value":"IQ"})
            df = df.drop_duplicates()
                    
            # 2 - select what we need and shaping
            # Please see "0_ResearchWork\4_SecondModel\ModelLSTM_Alex.ipynb" for more information
        
            features_considered = ['IQ','pressure','wind_direction','wind_force','humidity','temperature','NO2','O3','PM10']
            features = df[features_considered]
            features.index = df['date']
            
            print(features)

            dataset_test = features.values

            def higher_value(features,i):
                return[row[i] for row in dataset_test]

            max_pressure = max(higher_value(dataset_test,1))
            max_wind_force = max(higher_value(dataset_test,3))
            max_temperature = max(higher_value(dataset_test, 5))

            #normalize
            features['NO2'] = features['NO2'].apply(lambda x: x/10)
            features['O3'] = features['O3'].apply(lambda x: x/10)
            features['PM10'] = features['PM10'].apply(lambda x: x/10)
            
            features['pressure'] = features['pressure'].apply(lambda x: x/max_pressure)
            features['wind_force'] = features['wind_force'].apply(lambda x: x/max_wind_force)
            features['humidity'] = features['humidity'].apply(lambda x: x/100)
            features['temperature'] = features['temperature'].apply(lambda x: (x-273.15)/(max_temperature-273.15)) 

            # IQ dummy  
            dummy = pd.get_dummies(features['IQ'])
            IQDummy = pd.DataFrame(columns = range(1,11,1))
            IQDummy[dummy.columns] = dummy.fillna(0)

            iqlist = list(range(1,11,1))
            for i,r in enumerate(iqlist):
                iqlist[i] = "IQ"+str(r)
            IQDummy.columns = iqlist

            #wind_direction to categorical
            dummy = pd.get_dummies(features['wind_direction'])
            windDummy = pd.DataFrame(columns = range(0,361,10))
            windDummy[dummy.columns] = dummy.fillna(0)

            features = pd.concat([features, windDummy, IQDummy], axis=1)
            features = features.drop(columns=["wind_direction","IQ"])

            features = features.fillna(0)
        
            # 3- selecting the time period we need in the synop:
            # from the last 12:00 to the next "numberOfObservations" later
            countRow = 0
            x_pred = []
            for indexRow, rowx in features.iterrows():
                # for each day we found with a value at 12:00
                if indexRow.hour == 9:
                    # indexes for x (the range is inversed as our data are from the oldest to the newest)
                    batch = range(countRow, countRow - nbNeededObservation, -1)
                    #application
                    x_pred.append(features.iloc[batch].values)
                    dayConsidered = str(indexRow)[:10]
                    break
                countRow+=1
        except:
            Logger.log_error("Unable to shape the content for prediction")
            return(None)
            
        return(np.array(x_pred),dayConsidered)
        
        
    def postResult(self,y_pred,dayConsidered):
        """
        Post the result of the prediction in the API
        """
        dic = {"dayConsidered": dayConsidered}
        for i,pred in enumerate(y_pred):
            dic["J+{}".format(i+1)] = str(pred)
            
        response = requests.post(url = self.infos["URL"]+"realtimepredictions", json = dic)
        if not response.ok:
            Logger.log_error("Unable to POST the prediction")