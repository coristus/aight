## multiclass keras

import generateData as gd
import sortByLabel as sbl
import storyData as sd
import numpy as np
import pandas
from keras import metrics
from keras.models import Sequential
from keras.layers.core import Dropout
from keras.layers import Dense
from keras.layers.normalization import BatchNormalization
from keras.layers.convolutional import Conv1D
from keras.wrappers.scikit_learn import KerasClassifier
from keras.utils import np_utils
from sklearn.model_selection import cross_val_score
from sklearn.model_selection import KFold
from sklearn.preprocessing import LabelEncoder
from sklearn.preprocessing import LabelBinarizer
from sklearn.pipeline import Pipeline
from collections import Counter

# fix random seed for reproducibility
seed = 42
np.random.seed(seed)

SPLITSIZE = 10
labels, data = gd.getData()
TARGET = 'ISCO08_1'

labels, cleanCatData = sd.getCatData()
storiesData = sd.fillStoryIq(TARGET, labels, cleanCatData)
data = sd.construcDataFromArray(storiesData)

np.random.shuffle(data)

targetIdx = np.where(labels == TARGET)


# make test data from set of data with complete targets excluding full data
# sets (which are used for training)
Y_raw = data[:,targetIdx[0]]
deleteRowIndex = np.where(Y_raw == -1.0)
y_all = np.delete(Y_raw, deleteRowIndex[0], 0)


X_raw = np.delete(data, targetIdx[0], 1)
X_with_targets = np.delete(X_raw, deleteRowIndex[0], 0)

# X_no_targets = X_raw[deleteRowIndex[0],11:]


X = X_with_targets[:X_with_targets.shape[0]/5*4,11:]
y = y_all[:X_with_targets.shape[0]/5*4,:]


X_test = X_with_targets[X.shape[0]:,11:]
y_test = y_all[y.shape[0]:,:]


print X_test.shape
print y_test.shape
# encode class values as integers
encoder = LabelEncoder()
encoder.fit(y.flatten())
encoded_Y = encoder.transform(y.flatten())

encoder.fit(y_test.flatten())
encoded_Y_test = encoder.transform(y_test.flatten())

encoder.fit(y_all.flatten())
encoded_Y_all = encoder.transform(y_all.flatten())


# convert integers to dummy variables (i.e. one hot encoded)
dummy_y = np_utils.to_categorical(encoded_Y)
dummy_y_test = np_utils.to_categorical(encoded_Y_test)
dummy_y_all = np_utils.to_categorical(encoded_Y_all)

print(set(y.flatten()))
print dummy_y[1:10,]
# define baseline model
def buildModel(categories, trainingData):
    # create model
    model = Sequential()
    model.add(Dense(512, input_dim=(trainingData.shape[1]), activation='sigmoid'))
    model.add(Dropout(0.3, noise_shape=None, seed=None))
    # model.add(BatchNormalization(axis=-1, momentum=0.99,
    #     epsilon=0.001, center=True, scale=True, beta_initializer='zeros',
    #     gamma_initializer='ones', moving_mean_initializer='zeros',
    #     moving_variance_initializer='ones', beta_regularizer=None,
    #     gamma_regularizer=None, beta_constraint=None, gamma_constraint=None))
    # # #
    model.add(Dense(256, activation='sigmoid'))
    model.add(Dropout(0.3, noise_shape=None, seed=None))
    model.add(Dense(128, activation='sigmoid'))
    model.add(Dropout(0.2, noise_shape=None, seed=None))
    model.add(Dense(32, activation='sigmoid'))
    # model.add(Dropout(0.2, noise_shape=None, seed=None))
    model.add(Dense(10, activation='softmax'))
    # Compile model
    model.compile(loss='categorical_crossentropy', optimizer='adadelta', metrics=[metrics.mae, 'acc'])
    # model.compile(loss='categorical_crossentropy', optimizer='adadelta', metrics=[metrics.mae, metrics.categorical_accuracy])
    return model


#
# X_train = myData[0:myData.shape[0]-myData.shape[0]/(3*SPLITSIZE),]
# X_val = myData[X_train.shape[0]:X_train.shape[0]+myData.shape[0]/(2*SPLITSIZE),]
# X_test = myData[X_train.shape[0]+X_val.shape[0]:myData.shape[0],]
#
# dummy_train =  dummy_y[0:myData.shape[0]-myData.shape[0]/(3*SPLITSIZE),]
# dummy_val = dummy_y[X_train.shape[0]:X_train.shape[0]+myData.shape[0]/(2*SPLITSIZE),]
# dummy_test = dummy_y[X_train.shape[0]+X_val.shape[0]:myData.shape[0],]

TrainSet = X
TrainTargets = dummy_y
TestSet = X_test


model = buildModel(set(TrainTargets.flatten()), TrainSet)
# history = model.fit(TrainSet, TrainTargets, epochs=1000)
histroy = model.fit(TrainSet, TrainTargets, validation_data=(X_test,dummy_y_test), epochs=200)


y_pred = model.predict(X_test)





# sklearn estimator build
# estimator = KerasClassifier(build_fn=buildModel(10, myData), epochs=20, batch_size=256, verbose=1)
# kfold = KFold(n_splits=3, shuffle=True, random_state=seed)
# results = cross_val_score(estimator, myData, dummy_y)
# print 'class10 Classification: ' + str(results)
# print 'class10 Classification: ' + str(results.mean()*100) + ' ' + str(results.std()*100)
