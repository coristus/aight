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
from keras import regularizers
from keras.models import load_model




# fix random seed for reproducibility
seed = 21
np.random.seed(seed)

DATAPOINTS = 1000
SPLITSIZE = 10
# labels, data = gd.getData()
TARGET = 'ISCO08_1'

labels, cleanCatData = sd.getCatData()
targetColumnNr = np.where(labels == TARGET)[0][0]
# fill iq scores for better training
storiesData = sd.fillStoryIq(TARGET, labels, cleanCatData)
# Make balanced dataset
# balancedData = sd.categoryDataMaker(TARGET, labels, storiesData, 1000)

isoData = sd.isoDataMaker(storiesData)

# testdata = sd.construcDataFromArray(balancedData)

inlierData = sd.inlierDataMaker(TARGET, labels, isoData, DATAPOINTS, 2)
fakeData = sd.fakeDataMaker(TARGET, labels, inlierData, DATAPOINTS)
# standardData = sd.standardDataMaker(TARGET, labels, storiesData, DATAPOINTS, 6)
# categoryData = sd.categoryDataMaker(TARGET, labels, inlierData, DATAPOINTS)
data = sd.construcDataFromArray(fakeData)

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

X = X_with_targets[:X_with_targets.shape[0]/5*4,10:]
y = y_all[:X_with_targets.shape[0]/5*4,:]


X_test = X_with_targets[X.shape[0]:,10:]
y_test = y_all[y.shape[0]:,:]

### handle real data
realData = sd.construcDataFromArray(storiesData)
np.random.shuffle(realData)
real_Y_raw = realData[:,targetIdx[0]]
realDelIndex = np.where(real_Y_raw == -1.)

real_y = np.delete(real_Y_raw, realDelIndex[0], 0)
real_X_raw = np.delete(realData, targetIdx[0], 1)
real_X = np.delete(real_X_raw, realDelIndex[0], 0)[:,10:]


# encode class values as integers
encoder = LabelEncoder()
encoder.fit(y.flatten())
encoded_Y = encoder.transform(y.flatten())

encoder.fit(y_test.flatten())
encoded_Y_test = encoder.transform(y_test.flatten())

encoder.fit(y_all.flatten())
encoded_Y_all = encoder.transform(y_all.flatten())

LAYER_DENSITY = 384
# convert integers to dummy variables (i.e. one hot encoded)
dummy_y = np_utils.to_categorical(encoded_Y)
dummy_y_test = np_utils.to_categorical(encoded_Y_test)
dummy_y_all = np_utils.to_categorical(encoded_Y_all)
print dummy_y[0,:]
print(set(y.flatten()))
# define baseline model
def buildModel(categories, trainingData):
	# create model
	model = Sequential()
	# model.add(Dense(256, input_dim=(trainingData.shape[1]),
	#                 activity_regularizer=regularizers.l2(0.001), activation='sigmoid'))
	model.add(Dense(LAYER_DENSITY, input_dim=(trainingData.shape[1]), activation='relu'))
	model.add(Dropout(0.3, noise_shape=None, seed=None))
	model.add(Dense(LAYER_DENSITY/2, activation='relu'))
	model.add(Dropout(0.3, noise_shape=None, seed=None))
	model.add(Dense(LAYER_DENSITY/4, activation='relu'))
	model.add(Dropout(0.3, noise_shape=None, seed=None))
	    # # model.add(BatchNormalization(axis=-1, momentum=0.99,
    #     epsilon=0.001, center=True, scale=True, beta_initializer='zeros',
    #     gamma_initializer='ones', moving_mean_initializer='zeros',
    #     moving_variance_initializer='ones', beta_regularizer=None,
    #     gamma_regularizer=None, beta_constraint=None, gamma_constraint=None))
    # # # #
	# model.add(Dense(LAYER_DENSITY, activation='relu'))
	# model.add(Dropout(0.5, noise_shape=None, seed=None))
	# model.add(Dense(LAYER_DENSITY, activation='relu'))
	# model.add(Dropout(0.2, noise_shape=None, seed=None))
	# model.add(Dense(LAYER_DENSITY, activation='relu'))
	# model.add(Dropout(0.2, noise_shape=None, seed=None))
	# model.add(Dense(LAYER_DENSITY, activation='relu'))
	# model.add(Dropout(0.2, noise_shape=None, seed=None))

	model.add(Dense(categories, activation='softmax'))
	# Compile model
	model.compile(loss='categorical_crossentropy', optimizer='adadelta', metrics=['mae', 'acc'])
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

print 'Shape of trained data = ', str(X.shape), str(dummy_y.shape)
model = buildModel(len(set(TrainTargets.flatten())), TrainSet)
# history = model.fit(TrainSet, TrainTargets, epochs=1000)
histroy = model.fit(TrainSet, TrainTargets, validation_data=(X_test,dummy_y_test), batch_size=256, epochs=100)
model.save('100_ISCO08_1_384-192-96_iso_inlier.h5')  # creates a HDF5 file 'my_model.h5'

real_y_pred_classes = model.predict_classes(real_X)
print set(real_y_pred_classes)
# real_y_pred_classes = np_utils.probas_to_classes(real_y_pred_probas)
predictY = np.array(real_y_pred_classes)
trueY = real_y.flatten().astype(int)

print ' !!!!---- PREDICTIONS----!!!! '

a = predictY - trueY
print a[:100]
print len(np.nonzero(a)[0])
print len(a)







# sklearn estimator build
# estimator = KerasClassifier(build_fn=buildModel(10, myData), epochs=20, batch_size=256, verbose=1)
# kfold = KFold(n_splits=3, shuffle=True, random_state=seed)
# results = cross_val_score(estimator, myData, dummy_y)
# print 'class10 Classification: ' + str(results)
# print 'class10 Classification: ' + str(results.mean()*100) + ' ' + str(results.std()*100)
