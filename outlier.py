import numpy as np
import sklearn as sk
import generateData as gd
import sortByLabel as sbl
from sklearn.ensemble import IsolationForest as skiso
import time


rng = np.random.RandomState(42)
np.random.seed(1904)
TESTSIZE = 5
ESTIMATOR_RANGE = range(10, 251, 20)
MAX_SAMPLES_RANGE = range(10,1011,50)

(labels, data) = gd.getData()

catArrays, catLabels = sbl.splitByLabel('ISCO08_1', labels, data)

outlier_predictions_per_cat = []

for cat in catArrays:
    X = cat
    np.random.shuffle(X)
    X_train = X[0:X.shape[0]-X.shape[0]/TESTSIZE,]
    X_test = X[X_train.shape[0]:X.shape[0],]


    clf = skiso(n_estimators=ESTIMATOR_RANGE[0], max_samples=MAX_SAMPLES_RANGE[0], random_state=rng, n_jobs=-1)
    clf.fit(X_train)
    # y_pred_train = clf.predict(X_train)
    y_pred_test = clf.predict(X_test)
    y_pred_test.fill(0)
    for i in ESTIMATOR_RANGE:
        print str(i) + 'th estimator'
        for j in MAX_SAMPLES_RANGE:
            clf = skiso(n_estimators=i, max_samples=j, random_state=rng, n_jobs=-1)
            clf.fit(X_train)
            #y_pred_train = clf.predict(X_train)
            y_pred_test = y_pred_test+clf.predict(X_test)
    outlier_predictions_per_cat.append(y_pred_test)
np.save('outlier_predictions_per_cat.npy', np.array(outlier_predictions_per_cat))



# for kout in K_outliers:
#     print len(kout[0])

# y_pred_outliers = clf.predict(X_outliers)
