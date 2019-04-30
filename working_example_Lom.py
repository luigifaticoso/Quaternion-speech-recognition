#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Authors: Parcollet Titouan

import numpy                 as np

import keras                        
from   keras.optimizers      import Adam
from   models.example_model_Lom  import *
from   sklearn.preprocessing import normalize
import sys
import argparse              as Ap
import os

os.environ['KMP_DUPLICATE_LIB_OK']='True'


##########################################
###### UTILS FOR THE EXAMPLE_SCRIPT ######
##########################################

def dataPrepDecodaQuaternion(filename, isquat=True):

    nbTopics         = 250
    quaternionFactor = 4
    realChannel      = 3
    nbClasses        = 8
    raw              = open(filename, 'r').readlines()

    if(isquat):
        x            = np.ndarray(shape=(len(raw), nbTopics, quaternionFactor))
    else:
        x            = np.ndarray(shape=(len(raw), nbTopics, realChannel))
    y                = np.ndarray(shape=(len(raw), nbClasses))
    elementCpt       = 0
    documentCpt      = 0

    for doc in raw:
        elements   = doc.split('    ')[0].split(" ")
        nbElements = len(elements)

        # DATA
        for element in elements:
            components = element.split(',')
            if(isquat):
                x[documentCpt][elementCpt][0]   = float(components[0])
                x[documentCpt][elementCpt][1]   = float(components[1])
                x[documentCpt][elementCpt][2]   = float(components[2])
                x[documentCpt][elementCpt][3]   = float(components[3])
            else:
                x[documentCpt][elementCpt][0]   = components[1]
                x[documentCpt][elementCpt][1]   = components[2]
                x[documentCpt][elementCpt][2]   = components[3]

            elementCpt += 1
        elementCpt   = 0

        # LABELS
        labels   = doc.split('    ')[1].split(" ")
        labelCpt = 0
        for label in labels:
            values                   = label.split(',')
            y[documentCpt][labelCpt] = values[0]
            labelCpt                += 1
        labelCpt = 0
        documentCpt += 1
    return x,y


def getArgParser():
    parser = Ap.ArgumentParser(description='Parameters for the Neural Networks')
    
    parser.add_argument("--lr",             default="0.001",      type=float)
    parser.add_argument("--model", "--m",   default="QCNN",       type=str,
            choices=["QCNN", "QDNN", "CNN", "DNN"])

    args = parser.parse_args()
    return args

##########################################
######         MAIN PROGRAM         ######
##########################################

print('####################################################')
print('#     Quaternion Convolutional Neural Networks     #')
print('#      Parcollet Titouan - ORKIS - LIA - 2018      #')
print('####################################################')

params = getArgParser()

print('Data loading  -----------------------------')
if(params.model in ['QCNN' , 'QDNN']):
    x_train, y_train = dataPrepDecodaQuaternion('files_for_neural_Lom/TRAIN_process.data',isquat=True)
    x_dev,   y_dev   = dataPrepDecodaQuaternion('files_for_neural_Lom/DEV_process.data',  isquat=True)
    x_test,  y_test  = dataPrepDecodaQuaternion('files_for_neural_Lom/TEST_process.data', isquat=True)
else:
    x_train, y_train = dataPrepDecodaQuaternion('files_for_neural_Lom/TRAIN_process.data',isquat=False)
    x_dev,   y_dev   = dataPrepDecodaQuaternion('files_for_neural_Lom/DEV_process.data',  isquat=False)
    x_test,  y_test  = dataPrepDecodaQuaternion('files_for_neural_Lom/TEST_process.data', isquat=False)


print('Train size : '+str(x_train.shape[0]))
print('Dev size   : '+str(x_dev.shape[0]))
print('Test size  : '+str(x_test.shape[0]))

print('Parameters OPT SETTATO PRIMA A 0.0005-------------------------------')
opt = Adam(lr = 0.0005)
print('learning rate   : '+str(params.lr))
print('Model type      : '+str(params.model))


#
# CLASSIFIER
#

if(params.model in ['CNN' , 'QCNN']):
    classifier = CNN(params)
else:
    classifier = DNN(params)

print(' ')
print('Model Summary ----------------------------')
print(classifier.summary())

#
# Training
#
path = "./logging"
cbk = keras.callbacks.TensorBoard(path)

# Save Model
filepath = path + "/saved-model-{epoch:02d}-{val_acc:.2f}.hdf5"
checkpoint = keras.callbacks.ModelCheckpoint(filepath, monitor='val_acc', save_best_only=True, save_weights_only=False, mode='auto', period=1)

print("\nStarting training...")
classifier.compile(optimizer=opt, loss='categorical_crossentropy', metrics=['accuracy'])
classifier.fit(x_train, y_train,
                validation_data=(x_dev,y_dev),
                epochs=15,
                batch_size=15)

print("Training complete.\n")

# Save Path
classifier.save(path + "/saved_model.h5")
print("Saved model to disk")

#
# Eval.
#
print("\nEvaluating test...")
loss, acc = classifier.evaluate(x_test,y_test)

print('Test Loss = '+str(loss)+' | Test accuracy = '+str(acc))
print("That's All Folks :p ")
