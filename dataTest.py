import storyData as sd
import sortByLabel as sbl
from keras.models import load_model

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
import matplotlib.pyplot as plt


TARGET = 'ISCO08_1'
#
# labels, cleanCatData = sd.getCatData()
# storiesData = sd.fillStoryIq(TARGET, labels, cleanCatData)
# fakeData = sd.categoryDataMaker(TARGET, labels, storiesData, 5)

# for d in storiesData:
# 	print d.shape
# # sdata, slabels = sbl.splitForStory(TARGET, labels, cleanCatData)
# for s in fakeData:
#     print s.shape

# returns a compiled model
# identical to the previous one
# model = load_model('ISCO08_1.h5')
# model1 = load_model('ISCO08_1_256_256.h5')
# model = load_model('ISCO08_1_512_512_512.h5')
# model2 = load_model('ISCO08_1_deep_standard.h5')
# model2 = load_model('ISCO08_1_3deep1024_iso_inlier_standard.h5')
# model2 = load_model('ISCO08_1_7deep384_iso_inlier_standard.h5')
model2 = load_model('ISCO08_1_deep_standard.h5')
# model2 = load_model('ISCO08_1_384-192-96_iso_inlier_cate.h5')1
# model2 = load_model('ISCO08_1_2deep384_iso_inlier_standard.h5')
# seed = 42
# np.random.seed(seed)

TARGET = 'ISCO08_1'

labels, cleanCatData = sd.getCatData()
targetIdx = np.where(labels == TARGET)

# fill iq scores for better training
storiesData = sd.fillStoryIq(TARGET, labels, cleanCatData)
standardData = sd.categoryDataMaker(TARGET, labels, storiesData, 5)
realData = sd.construcDataFromArray(standardData)
np.random.shuffle(realData)
real_Y_raw = realData[:,targetIdx[0]]
realDelIndex = np.where(real_Y_raw == -1.)
real_y = np.delete(real_Y_raw, realDelIndex[0], 0)
real_X_raw = np.delete(realData, targetIdx[0], 1)
real_X = np.delete(real_X_raw, realDelIndex[0], 0)[:,10:]


real_y_pred_classes = model2.predict_classes(real_X)
prob_pred = model2.predict(real_X)

prob_sort = np.argsort(prob_pred, axis=1)
best = prob_sort[:,-3:]

# real_y_pred_classes = np_utils.probas_to_classes(real_y_pred_probas)
predictY = np.array(real_y_pred_classes)
trueY = real_y.flatten().astype(int)
correctIdx = np.where((predictY-trueY)==0)[0]
correct = trueY[correctIdx]
a = np.bincount(correct)
b = np.bincount(trueY)
percentages = np.array(a, dtype='float64')/np.array(b, dtype='float64')


print '\n\n\n'
count = 0
for y in range(len(trueY)):
	if trueY[y] in best[y,:]:
		count += 1
print count/float(len(trueY))*100


N = 10


ind = np.arange(N)  # the x locations for the groups
width = 0.35       # the width of the bars

fig, ax = plt.subplots()
rects1 = ax.bar(ind, a, width, color='g')

rects2 = ax.bar(ind + width, b, width, color='r')

# add some text for labels, title and axes ticks
ax.set_ylabel('Count')
ax.set_title('Classified per category')
ax.set_xticks(ind + width / 2)
ax.set_xticklabels(('0', '1', '2', '3', '4', '5', '6', '7', '8', '9'))

ax.legend((rects1[0], rects2[0]), ('Right', 'Total'))


def autolabel(rects):
    """
    Attach a text label above each bar displaying its height
    """
    for rect in rects:
        height = rect.get_height()
        ax.text(rect.get_x() + rect.get_width()/2., 1.05*height,
                '%d' % int(height),
                ha='center', va='bottom')

autolabel(rects1)
autolabel(rects2)

plt.show()

# print ' !!!!---- PREDICTIONS----!!!! '
# person = 1555
# multi = 1
# real_1_predict = model1.predict_classes(real_X[person:person+multi,:])
# real_2_predict = model2.predict_classes(real_X[person:person+multi,:])
# real_1_y = real_y[person:person+multi]
# print 'predicted and real category'
# print real_2_predict, real_1_y.flatten()
# a = predictY - trueY
#
#
# chances1_are = model1.predict(real_X[person:person+multi,:])
# chances2_are = model2.predict(real_X[person:person+multi,:])
#
# print 'chances per category'
# perc1 = chances1_are[0].flatten()*100
# perc2 = chances2_are[0].flatten()*100
# print np.around(perc1)
# print np.around(perc2)
