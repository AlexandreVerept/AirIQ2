# Program use by the Frontend API to connect to the database and make requests

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
            
    
    def getAllPredictions(self):
        """
        retrieve all the predictions from te database
        """
        try:
            with self.connection.cursor() as cursor:
                sql = "SELECT value,dateofprediction,typeofprediction FROM predictiontable ORDER BY dateofprediction DESC"
                cursor.execute(sql)
                result = cursor.fetchall()
                df = pd.DataFrame(result)
        except:
            Logger.log_error("Unable to do the query in 'getAllPredictions'")
            return(None)
        return(df.to_dict())
        
        
    def getLastsPredictions(self,numberOfDays):
        """
        retrieve all the predictions from te database for the x last days
        """
        try:
            with self.connection.cursor() as cursor:
                sql = f"SELECT value,dateofprediction,typeofprediction,insertdate FROM predictiontable WHERE insertdate >= (CURDATE() - INTERVAL {numberOfDays} DAY) ORDER BY dateofprediction DESC;"
                cursor.execute(sql)
                result = cursor.fetchall()
                df = pd.DataFrame(result)
        except:
            Logger.log_error("Unable to do the query in 'getAllPredictions'")
            return(None)
        return(df.to_dict())