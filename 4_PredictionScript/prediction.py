import tensorflow as tf
from tensorflow import keras
from keras.models import Model
from keras.models import load_model

class predictionMaker():
    """
    this class allow us to make the prediction
    """
    def __init__(self,modelPath="Models/modelProduction.h5"):
        self.model = load_model(modelPath)
        
    def reloadModel(self,modelPath="Models/modelProduction.h5"):
        """
        force to load a new model
        """
        self.model = load_model(modelPath)
        
    def makePrediction(self,x_to_pred):
        """
        make a prediction
        params: data needed for the prediction
        return: prediction
        """
        y_pred = self.model.predict(x_to_pred)
        print(y_pred)
        return(y_pred)