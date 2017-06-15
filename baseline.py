#baseline classifier on function group.
import generateData as gd
import numpy as np
from sklearn.neural_network import MLPClassifier as mlp
from sklearn.multiclass import OneVsRestClassifier
from sklearn.svm import LinearSVC
from sklearn.preprocessing import MultiLabelBinarizer

labels, data = gd.getData()

targetIdx = np.where(labels == 'ISCO08_1')
Y_raw = data[:,targetIdx[0]]
deleteRowIndex = np.where(Y_raw == -1.0)
y = np.delete(Y_raw, deleteRowIndex[0], 0)

X_raw = np.delete(data, targetIdx[0], 1)
X = np.delete(X_raw, deleteRowIndex[0], 0)

mlb = MultiLabelBinarizer()
Y_bin = mlb.fit_transform(y)

print X.shape
print y.shape

# algorithm = mlp(solver='adam', alpha=1e-8, hidden_layer_sizes=(64, 64), random_state=1)

results = OneVsRestClassifier(LinearSVC(random_state=0),n_jobs=-1).fit(X, y).predict(X)
# results = OneVsRestClassifier(algorithm).fit(X, Y_bin).predict(X)
failed = np.count_nonzero(np.array(results)-y.T)
print 'percentage classified right = ' + str((1. -failed/float(len(results))) *100)

# all_labels = mlb.inverse_transform(results)
