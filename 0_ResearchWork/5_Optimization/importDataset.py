# This script is use to import the dataset (see our notebook in 4_SecondModel for more details)

import numpy as np
import pandas as pd
from sklearn.utils import shuffle

RANDOM_SHUFFLE_SEED = 0

#dataset
CSV_PATH = "dataset/"
CSV_NAME = "completeDataset.csv"
features_considered = ['IQ','pressure','wind_direction','wind_force','humidity','temperature']

DF = pd.read_csv(CSV_PATH+CSV_NAME, header=0, delimiter=';')
DF['date'] = pd.to_datetime(DF['date'],utc=True)

def importData(nb_prev_measures_for_predict):
    print("=====IMPORT=====")
    features = DF[features_considered]
    features.index = DF['date']

    dataset_test = features.values

    def higher_value(features,i):
        return[row[i] for row in dataset_test]

    max_pressure = max(higher_value(dataset_test,1))
    max_wind_force = max(higher_value(dataset_test,3))
    max_temperature = max(higher_value(dataset_test, 5))

    #normalize
    features['IQ'] = features['IQ'].apply(lambda x: x/10)
    features['pressure'] = features['pressure'].apply(lambda x: x/max_pressure)
    features['wind_force'] = features['wind_force'].apply(lambda x: x/max_wind_force)
    features['humidity'] = features['humidity'].apply(lambda x: x/100)
    features['temperature'] = features['temperature'].apply(lambda x: (x-273.15)/(max_temperature-273.15)) 

    #wind_direction to categorical
    features = pd.concat([features, pd.get_dummies(features['wind_direction'])], axis=1)
    features = features.drop(columns=["wind_direction"])

    x_train = []
    y_train = []
    countRow=0

    for indexRow, rowx in features.iterrows():
        # for each day we found with a value at 12:00
        if indexRow.hour == 12 and countRow >= nb_prev_measures_for_predict:
            try:
                # indexes for x (the range is inversed as our data are from the oldest to the newest)
                batchX = range(countRow, countRow - nb_prev_measures_for_predict, -1)
                # indexes for y
                batchY = [countRow+8,countRow+16,countRow+24]

                #application
                y_train.append(features.iloc[batchY]["IQ"].values)
                x_train.append(features.iloc[batchX].values)
            except:
                print("To long for ",indexRow)
        countRow+=1
    
    x_train = np.array(x_train)
    y_train = np.array(y_train)
    
    x_train,y_train = shuffle(x_train,y_train, random_state=RANDOM_SHUFFLE_SEED)
    
    x_train = np.array(x_train)
    y_train = np.array(y_train)
    y_train = y_train.reshape(y_train.shape[0],3,1)
    print("x_train :",x_train.shape)
    print("y_train :",y_train.shape)
    
    print("====END IMPORT====")
    return(x_train,y_train)

