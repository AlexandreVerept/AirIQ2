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
        send informations needed to make the prediction (3 previous days):
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
                dfiq = pd.DataFrame(result)
        except:
            Logger.log_error("Unable to do the IQ query in 'getInformationsDataCollector'")
            return(None)
            
        # 2 - the main pollutants
        # TODO when the shape of the data will be define
        
        
        
        # 3 - synop data
        try:
            with self.connection.cursor() as cursor:
                sql = "SELECT pressure,wind_direction,wind_force,temperature,humidity,date FROM synoptable WHERE date >= (CURDATE() - INTERVAL 2 DAY) ORDER BY date DESC"
                cursor.execute(sql)
                result = cursor.fetchall()
                dfsynop = pd.DataFrame(result)
        except:
            Logger.log_error("Unable to do the IQ query in 'getInformationsDataCollector'")
            return(None)
            
        return(dfiq.to_dict(),dfsynop.to_dict())
            
    
    def postRealTimePredictions(self, request): # TODO !!!!
        """
        collect predictions of the index quality from the script python dedicated to this task and put it in the DB
        """
        
        """
        if not request:
            return(None)
        try:
            #récupérer l'indice de qualité de l'air et le jour associé dans le script (pas encore créé donc je ne sais pas comment le récupérer)
            with self.connection.cursor() as cursor:
                sql = "INSERT INTO predictiontable(value,dateofprediction) "
                cursor.execute(sql)
        except:
            Logger.log_error("Unable to do the query in 'postRealTimePredictions'")
            return(None)"""
            
        return("lol")
        
     
    def postInformationsDataCollector(self, request, typeOfValue):
        """
        collect all datas from the data collector to put into the DB
        """
        
        def saveRow(row,typeOfValue):
            """
            request to put a row of iq data in the db
            """
            try:
                # define the query
                if typeOfValue=="iq":
                    sql = 'INSERT INTO iqtable(date,value) VALUES (%s, %s);'
                    val = (str(row["date"]), row["value"])
                elif typeOfValue=="synop":
                    sql = 'INSERT INTO synoptable(date,pressure,wind_direction,wind_force,humidity,temperature) VALUES (%s, %s, %s, %s, %s, %s);'
                    val = (row["date"], row["pressure"], row["wind_direction"], row["wind_force"], row["humidity"], row["temperature"])
                elif typeOfValue=="pollutant":
                    print("pollutant not yet implemented !") # TODO
                    
                else:
                    raise ValueError('Wrong type of value')
                    
                # execute the query
                with self.connection.cursor() as cursor:
                    cursor.execute(sql,val)
                    self.connection.commit()
            except Exception as e:
                if (type(e).__name__) == "IntegrityError": # this exception occur when there is a dupplicate line
                    print("Already in database ?",val)
                else:
                    Logger.log_error(f"Unable to do the query in 'dataBaseConnector - postInformationsDataCollector'")

        # put the request in a dataframe    
        df = pd.DataFrame.from_dict(request)
        # execute a request for each row
        df.apply(lambda x: saveRow(x,typeOfValue),axis=1)            
        return("ok")
        