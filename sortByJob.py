# Sorts data by job categorie.

import numpy as np
import generateData as gd

##
# Jobs are in ISCO08_1
# input labels, find job category and create set of jobs
def splitByLabel(label, labels, data):
    returnArray = []
    returnArrayLabels = []
    index = np.where(labels == label)
    category = set(data[:,index].flatten())

    # Create a numpy array per job category (ISCO08_1) and save as array
    for category in categories:
        select = np.where(data[:,index[0][0]] == category)
        returnArrayLabels.append(category)
        returnArray.append(data[select[0]])
        np.save('full/job_' + str(category) + '.npy', data[select[0]])
    return (np.array(returnArray), returnArrayLabels)
