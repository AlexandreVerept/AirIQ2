import tensorflow as tf
from tensorflow import keras
from keras.models import Model
from keras.models import load_model
from logger import Logger
import numpy as np

class predictionMaker():
    """
    this class allow us to make the prediction
    """
    def __init__(self,modelPath="Models/modelProduction.h5"):
        self.reloadModel(modelPath)
        
    def reloadModel(self,modelPath="Models/modelProduction.h5"):
        """
        force to load a new model
        """
        try:
            self.model = load_model(modelPath)
        except:
            Logger.log_error("Unable to load the model in the predictionMaker")
        
    def makePrediction(self,x_pred):
        """
        make a prediction
        params: data needed for the prediction
        return: prediction
        """
        y_pred = self.model.predict(x_pred)
        return(np.array(y_pred).reshape(3))