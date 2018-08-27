import matplotlib
matplotlib.use('Agg')
import numpy as np
import pandas as pd
from pandas import Series,DataFrame
import re 
import os
from os import environ
from matplotlib import pyplot as plt
import matplotlib.gridspec as gridspec

from keras import backend as K
K.clear_session()
from keras.models import Model,Sequential
from keras.layers import Input, Dense, Flatten, Dropout, Activation
from keras.layers import LSTM, SimpleRNN,LeakyReLU
from keras.callbacks import LearningRateScheduler, ModelCheckpoint, TensorBoard
from keras import regularizers

'''
with the input_step_size and output_size ,you can define the number of predict and previuos data when the model deployed
'''
data = pd.read_csv('wktest-master/water-tilt.csv')  #load data
input_step_size = 50  #data transform input shape 
output_size = 10   #data transform output shap

'''
get WML environment and define the out_path
'''
model_filename = "lstm.json"
picname = 'pred_act.png'
weight_file = 'weight.hdf5'

if environ.get('RESULT_DIR') is not None:
    output_model_folder = os.path.join(os.environ["RESULT_DIR"], "model")
    output_model_path = os.path.join(output_model_folder, model_filename)
    output_pic_folder = os.path.join(os.environ["RESULT_DIR"], "picture")
    output_pic_path = os.path.join(output_pic_folder, picname)
    output_weight_folder = os.path.join(os.environ["RESULT_DIR"], "weight")
    output_weight_path = os.path.join(output_weight_folder, weight_file)    
else:
    output_model_folder = "model"
    output_model_path = os.path.join("model", model_filename)
    output_pic_folder = "picture"
    output_pic_path = os.path.join("picture", picname)
    output_weight_folder = "weight"
    output_weight_path = os.path.join("weight", weight_file)

os.makedirs(output_model_folder, exist_ok=True)
os.makedirs(output_pic_folder, exist_ok=True)
os.makedirs(output_weight_folder, exist_ok=True)

'''
transform datasets return x_train, y_train, x_val, y_val, x_test, y_test
'''
def dataset_setup(data):
    data = np.array(data)
    inputs = []
    outputs = []
    for i in range(len(data)-input_step_size-output_size):
        inputs.append(data[i:i + input_step_size])   #
        outputs.append(data[i + input_step_size: i + input_step_size+ output_size])
    inputs = np.array(inputs)
    outputs = np.array(outputs)
    size1 = int(0.8*inputs.shape[0])
    size2 = int(0.9*inputs.shape[0])
    x_train  = inputs[:size1,:]
    y_train = outputs[:size1,:,-1]
    x_val = inputs[size1:size2,:]
    y_val = outputs[size1:size2,:,-1]
    x_test = inputs[size2:,:]
    y_test = outputs[size2:,:,-1]
    plt.figure(figsize=(100,10))
    plt.plot(DataFrame(data))
    plt.savefig('./out_th.png')
    plt.clf()
    return x_train, y_train, x_val, y_val, x_test, y_test

'''
create model with three lstm layer 
'''
def create_model(x_train):
    m_inputs = Input(shape=(x_train.shape[1],x_train.shape[2]))
    lstm1 = LSTM(units=128, return_sequences=True)(m_inputs)#128
    lstm2 = LSTM(units=64,return_sequences=True)(lstm1)#64
    lstm3 = LSTM(units=32,return_sequences=True)(lstm2)#32
    fa = Flatten()(lstm3)
    out = Dense(10)(fa)
    model = Model(m_inputs,out)
    model.compile(loss='mae', optimizer='adam')
    return model

'''
train and save the model,plot the result and save as a png file
'''
def train_and_test_model(model,x_train, y_train, x_val, y_val, x_test, y_test):
    learn_rate = lambda epoch: 0.0001 if epoch < 10 else 0.00001
    callbacks = [LearningRateScheduler(learn_rate)]
    callbacks.append(ModelCheckpoint(filepath=output_weight_path, monitor='val_loss', save_best_only=True))	
    history = model.fit(x_train, y_train, epochs=50, batch_size=16, validation_data=(x_val, y_val), verbose=1, shuffle=False, callbacks=callbacks)
    json_string = model.to_json()
    with open(output_model_path, "w") as f:
        f.write(json_string)
    plt.plot(history.history['loss'], label='train')
    plt.plot(history.history['val_loss'], label='val')
    plt.legend()
    plt.savefig(os.path.join(output_pic_folder,'loss.png'))
    y_pred = model.predict(x_test)
    x = [i for i in range(y_pred.shape[0])]
    ax1 = plt.subplot(211)
    ax1.set_title('predict')
    ax1.plot(x,y_pred[:,0])
    ax2=plt.subplot(212)
    ax2.set_title('active')
    ax2.plot(x,y_test[:,0])
    plt.tight_layout(2)
    plt.savefig(output_pic_path)


if __name__ == '__main__':
    x_train, y_train, x_val, y_val, x_test, y_test = dataset_setup(data.iloc[:,1:])
    model = create_model(x_train)
    train_and_test_model(model,x_train, y_train, x_val, y_val, x_test, y_test)

