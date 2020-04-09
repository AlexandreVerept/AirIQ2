# Program use by the Backend API to connect to the database and make requests

import pymysql.cursors
import pandas as pd
import json
from logger import Logger
from datetime import datetime, date, timedelta

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
            
            
    def getDataNeededPrediction(self,x):
        """
        send informations needed to make the prediction (x previous days):
            - the IQ
            - main pollutants (not yet implemented)
            - synop data
        """
        
        # 1 - the IQ:
        try:
            with self.connection.cursor() as cursor:
                sql = f"SELECT value,date FROM iqtable WHERE date >= (CURDATE() - INTERVAL {x} DAY) ORDER BY date DESC"
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
                sql = f"SELECT pressure,wind_direction,wind_force,temperature,humidity,date FROM synoptable WHERE date >= (CURDATE() - INTERVAL {x} DAY) ORDER BY date DESC"
                cursor.execute(sql)
                result = cursor.fetchall()
                dfsynop = pd.DataFrame(result)
        except:
            Logger.log_error("Unable to do the IQ query in 'getInformationsDataCollector'")
            return(None)
            
        return(dfiq.to_dict(),dfsynop.to_dict())
            
    
    def postRealTimePredictions(self, request):
        """
        collect predictions of the index quality from the script python dedicated to this task and put it in the DB
        """
        if not request:
            return(None)
        else:
            dayConsidered = datetime.strptime(request["dayConsidered"], '%Y-%m-%d')
        try:
            for i in range(1,4):
                val = (float(request[f"J+{i}"])*10, str(dayConsidered + timedelta(days=i)), f"J+{i}", str(date.today()))
                
                with self.connection.cursor() as cursor:
                    sql = "INSERT INTO predictiontable(value,dateofprediction,typeofprediction,insertdate) VALUES (%s, %s, %s, %s);"
                    cursor.execute(sql,val)
                    self.connection.commit()
        except:
            Logger.log_error("Unable to do the query in 'postRealTimePredictions'")
            return(None)
            
        return("ok")
        
     
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
                    #print("Already in database ?",val)
                    None
                else:
                    Logger.log_error(f"Unable to do the query in 'dataBaseConnector - postInformationsDataCollector'")

        # put the request in a dataframe    
        df = pd.DataFrame.from_dict(request)
        # execute a request for each row
        df.apply(lambda x: saveRow(x,typeOfValue),axis=1)            
        return("ok")
        
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
                df['dateofprediction'] = df['dateofprediction'].astype(str)
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
                df['dateofprediction'] = df['dateofprediction'].astype(str)
        except:
            Logger.log_error("Unable to do the query in 'getAllPredictions'")
            return(None)
        return(df.to_dict())
        