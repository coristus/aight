# Sorts data by label.

import numpy as np
import generateData as gd

##
# Jobs are in ISCO08_1
# input label (target) and set of labels (for positioning column + clean data)
# def splitByLabel(label, labels, data):
#     returnArray = []
#     returnArrayLabels = []
#     index = np.where(labels == label)
#     categories = set(data[:,index].flatten())
#     try:
#         categories.remove(-1.0)
#     except ValueError:
#         pass
#
#     # Create a numpy array per job category (ISCO08_1) and save as array
#     for category in categories:
#         select = np.where(data[:,index[0][0]] == category)
#         returnArrayLabels.append(category)
#         returnArray.append(data[select[0]])
#     return (np.array(returnArray), returnArrayLabels)


def splitForStory(label, labels, data):
    returnArray = []
    returnArrayLabels = []
    index = np.where(labels == label)
    categories = set(data[:,index[0]].flatten())
    # Create a numpy array per job category (ISCO08_1) and save as array
    for category in categories:
        select = np.where(data[:,index[0][0]] == category)
        returnArrayLabels.append(category)
        returnArray.append(data[select[0]])
    return np.array(returnArray), returnArrayLabels


## Input a list of selected labels and dataset to work on
#  assumes 2d numpy array input and list of labels
#  returns all colums as an np array
def selectColumns(selectLabels, data):
    idList = []
    npLabels = np.array(selectLabels)
    for label in selectLabels:
        idList.append(np.where(npLabels == label)[0][0])
    return data[:, idList]
