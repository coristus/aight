#plot outliers
import matplotlib.pyplot as pl
import numpy as np

## Variables
TESTSIZE = 5
ESTIMATOR_RANGE = range(10, 251, 20)
MAX_SAMPLES_RANGE = range(10,1011,50)
MAX_SCORE = (len(ESTIMATOR_RANGE)*len(MAX_SAMPLES_RANGE))
MIN_SCORE =-(len(ESTIMATOR_RANGE)*len(MAX_SAMPLES_RANGE))

## Load predicted test outliers
outlier_predictions_per_cat = np.load('outlier_predictions_per_cat.npy')

i = 0
for y_pred_test in outlier_predictions_per_cat:
    K_outliers = []
    length_outliers = []
    for k in range(MIN_SCORE,MAX_SCORE,1):
        outliers = np.where(y_pred_test <= k)
        K_outliers.append(len(outliers[0])/float(y_pred_test.shape[0])*100)

    pl.subplot(2,3,i+1)
    pl.plot(range(MIN_SCORE,MAX_SCORE,1), K_outliers,'r.')
    pl.title('Job category ' + str(i) + ' Subjects: ' + str(y_pred_test.shape[0]))
    pl.ylabel('Percentage of Outliers')
    pl.ylim((0,70))
    i+=1
    if i == 6: break
pl.show()
