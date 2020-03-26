from importDataset import importData

from keras.optimizers import RMSprop,Adam
from keras.callbacks import TensorBoard
from time import time
from keras.models import Model
from keras.layers import LSTM, Dense, Input

from keras.models import save_model

PATH_TO_MODELS = "Models/"

# PARAMS TO TEST
EPOCHS = 200
LR = 0.0005

NUMBER_OBSERVATIONS = [24,36,80]
LSTM_HIDDEN_UNITS = [32,128,512,1024]
INTERMEDIATE_DENSE = [0,128,512,1024]
OPTIMIZER = {"RMS" : RMSprop(LR),"Adam":Adam(LR)}

if __name__ == '__main__':
    for observations in NUMBER_OBSERVATIONS:
        x_train,y_train = importData(observations)
        
        trainLength = int(len(x_train)*0.8)
        
        x,x_val = x_train[:trainLength],x_train[trainLength:]
        y,y_val = y_train[:trainLength],y_train[trainLength:]
        
        for opti in OPTIMIZER:
            for hiddenUnit in LSTM_HIDDEN_UNITS:
                for denseSize in INTERMEDIATE_DENSE:
                    name = f"nobs{observations}-opti{opti}-lr{LR}-hid{hiddenUnit}-dens{denseSize}-time{int(time())}"
                    print(name)
                    try:
                        callbackName = str('.\logs\\{}'.format(name))
                        tensor_board = TensorBoard(callbackName)

                        input_shape = (x_train.shape[-2],x_train.shape[-1])
                        inp = Input(input_shape)
                        d = LSTM(hiddenUnit,input_shape=input_shape,name='LSTM_layer')(inp)
                        if denseSize>0:
                            d = Dense(denseSize,name="Intermediate_dense_layer")(d)
    
                        outD1 = Dense(1,name="D1")(d)
                        outD2 = Dense(1,name="D2")(d)
                        outD3 = Dense(1,name="D3")(d)
    
                        model = Model(inputs=[inp], outputs=[outD1, outD2, outD3])    
                        model.compile(optimizer=OPTIMIZER[opti], loss={'D1': 'mse', 'D2': 'mse', 'D3': 'mse'}, metrics={'D1': 'mae', 'D2': 'mae', 'D3': 'mae'})
                    
                        model.fit(x=x, y=[y[:,0],y[:,1],y[:,2]], validation_data=(x_val,[y_val[:,0],y_val[:,1],y_val[:,2]]),epochs=EPOCHS,callbacks = [tensor_board])
                    
                        #save_model(model, PATH_TO_MODELS+"/"+name+".h5", overwrite=True, include_optimizer=True)
                    except:
                        print("Error: ",name)