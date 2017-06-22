import numpy as np
import sklearn as sk
import generateData as gd
import sortByLabel as sbl
import storyData as sd
from sklearn.ensemble import IsolationForest as skiso
import time


rng = np.random.RandomState()
# np.random.seed(1904)
TESTSIZE = 3
ESTIMATOR_RANGE = range(10, 251, 20)
MAX_SAMPLES_RANGE = range(200,201,50)

labels, data = sd.getCatData()

catArrays, catLabels = sbl.splitForStory('ISCO08_1', labels, data)


def isoDataMaker(catArray):
	outlier_predictions_per_cat = []
	dataSet = []
	for cat in catArrays:
		X = cat[:,11:]
		print X.shape[1]
		np.random.shuffle(X)
		clf = skiso(n_estimators=20, random_state=rng, n_jobs=-1)
		clf.fit(X)
		predicted = clf.predict(X)
		abnormal = X[predicted == -1]
		normal = X[predicted == 1]
		print normal.shape
		print abnormal.shape
		outlier_predictions_per_cat.append(predicted)
		dataSet.append(normal)
	return dataSet, outlier_predictions_per_cat




np.save('outlier_predictions_per_cat_1.npy', np.array(outlier_predictions_per_cat))



# for kout in K_outliers:
#     print len(kout[0])

# y_pred_outliers = clf.predict(X_outliers)
