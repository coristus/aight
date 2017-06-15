## multiclass keras

import generateData as gd
import sortByLabel as sbl
import numpy as np
import pandas
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
from sklearn.pipeline import Pipeline


# fix random seed for reproducibility
seed = 42
np.random.seed(seed)

labels, data = gd.getData()
TARGET = 'ISCO08_1'
# make target of selected column for classification and delete all rows with no
# entry (set to -1)
targetIdx = np.where(labels == TARGET)
Y_raw = data[:,targetIdx[0]]
deleteRowIndex = np.where(Y_raw == -1.0)
y = np.delete(Y_raw, deleteRowIndex[0], 0)

# create dataset matching targeted column without target column
X_raw = np.delete(data, targetIdx[0], 1)
X_all_features = np.delete(X_raw, deleteRowIndex[0], 0)

# # select columns that you want
X_selected = sbl.selectColumns(['T_Invloed', 'T_Prestatie', 'T_Welvaart', 'T_Plezier', 'T_Avontuur',
 'T_Vrijheid', 'T_Dialoog', 'T_Zorg', 'T_Team', 'T_Rechtvaardigheid',
 'T_Traditie', 'T_Zekerheid', 'TTN1', 'TTN2', 'TTN3', 'TTN4', 'TTN5', 'TTE1',
 'TTE2', 'TTE3', 'TTE4', 'TTE5', 'TTO1', 'TTO2', 'TTO3', 'TTO4', 'TTA1', 'TTA2',
 'TTA3', 'TTA4', 'TTA5', 'TTC1', 'TTC2', 'TTC3', 'TTC4', 'TTC5', 'Tscore_BA'], X_all_features)

# X_selected = sbl.selectColumns(['TTN1', 'TTN2', 'TTN3', 'TTN4', 'TTN5', 'TTE1',
#   'TTE2', 'TTE3', 'TTE4', 'TTE5', 'TTO1', 'TTO2', 'TTO3', 'TTO4', 'TTA1', 'TTA2',
#   'TTA3', 'TTA4', 'TTA5', 'TTC1', 'TTC2', 'TTC3', 'TTC4', 'TTC5'], X_all_features)
print X_selected.shape

## remove all incomplete columns.. too rigorous.
# minus1_idx = np.where(X_all_features == -1)
# X_only_full = np.delete(X_all_features, minus1_idx, 1)

# encode class values as integers
encoder = LabelEncoder()
encoder.fit(y.flatten())
encoded_Y = encoder.transform(y.flatten())
# convert integers to dummy variables (i.e. one hot encoded)
dummy_y = np_utils.to_categorical(encoded_Y)

# define baseline model
def class10_model():
    # create model
    model = Sequential()
    model.add(Dense(128, input_dim=(X_all_features.shape[1]), activation='sigmoid'))
    model.add(Dropout(0.2, noise_shape=None, seed=None))
    model.add(BatchNormalization(axis=-1, momentum=0.99,
        epsilon=0.001, center=True, scale=True, beta_initializer='zeros',
        gamma_initializer='ones', moving_mean_initializer='zeros',
        moving_variance_initializer='ones', beta_regularizer=None,
        gamma_regularizer=None, beta_constraint=None, gamma_constraint=None))
    #
    # model.add(Dense(96, activation='sigmoid'))
    # model.add(Dropout(0.2, noise_shape=None, seed=None))
    # model.add(Dense(64, activation='sigmoid'))
    # model.add(Dropout(0.2, noise_shape=None, seed=None))
    # model.add(Dense(32, activation='sigmoid'))
    # model.add(Dropout(0.3, noise_shape=None, seed=None))
    model.add(Dense(10, activation='softmax'))
    # Compile model
    model.compile(loss='categorical_crossentropy', optimizer='adadelta', metrics=['accuracy'])
    return model

estimator = KerasClassifier(build_fn=class10_model, epochs=200, batch_size=256, verbose=1)

kfold = KFold(n_splits=3, shuffle=True, random_state=seed)

results = cross_val_score(estimator, X_all_features, dummy_y, cv=kfold)
print 'class10 Classification: ' + str(results)
print 'class10 Classification: ' + str(results.mean()*100) + ' ' + str(results.std()*100)
