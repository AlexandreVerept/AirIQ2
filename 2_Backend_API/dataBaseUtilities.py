# Program use by the Backend API to connect to the database and make requests

import pymysql.cursors
import pandas as pd
import json
from logger import Logger

class dataBaseConnector():
    def __init__(self):        
        # retrieve informations needed to connect to the database
        try:
            with open('db_informations.json') as json_file:
                self.infos = json.load(json_file)
        except:
            Logger.log_error("Unable to find/open 'db_informations.json' for the connection to the database")
            return(None)
        
        # create a cursor
        try:
            self.connection=pymysql.connect(host=self.infos["host"],
                               user=self.infos["user"],
                               passwd=self.infos["passwd"],
                               db=self.infos["db"],
                               cursorclass=pymysql.cursors.DictCursor)
        except:
            Logger.log_error("Unable to create a cursor for the connection with the database")
            return(None)
            
            
    def getInformationsDataCollector(self):
        """
        send informations needed to make the prediction (2 previous days):
            - the IQ
            - main pollutants (not yet implemented)
            - synop data
        """
        
        # 1 - the IQ:
        try:
            with self.connection.cursor() as cursor:
                sql = "SELECT value,date FROM iqtable WHERE date >= (CURDATE() - INTERVAL 2 DAY) ORDER BY date DESC"
                cursor.execute(sql)
                result = cursor.fetchall()
                df = pd.DataFrame(result)
        except:
            Logger.log_error("Unable to do the IQ query in 'getInformationsDataCollector'")
            return(None)
            
            
            
        return(df.to_dict())

            
            
            
            
            
            
            
            
    
    def postRealTimePredictions(self):
        """
        collect predictions of the index quality from the script python dedicated to this task and put it in the DB
        """
        try:
            #récupérer l'indice de qualité de l'air et le jour associé dans le script (pas encore créé donc je ne sais pas comment le récupérer)
            with self.connection.cursor() as cursor:
                sql = "INSERT INTO predictiontable(value,dateofprediction) "
                cursor.execute(sql)
        except:
            Logger.log_error("Unable to do the query in 'getRealTimePredictions'")
            return(None)
        return(df.to_dict())
        
     
    def postInformationsDataCollector(self):
        """
        collect all datas from the data collector to put into the DB
        """
        try : 
            #récupérer les datas du data collector
            with self.connection.cursor() as cursor:
                sql = ""
                cursor.execute(sql)
        except:
            Logger.log_error("Unable to do the query in 'getInformationsDataCollector'")
            return (None)
        return (df.to_dict())