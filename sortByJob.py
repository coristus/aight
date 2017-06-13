# Sorts data by job categorie.

import numpy as np
import generateData as gd

(labels, data) = gd.getData()

##
# Jobs are in ISCO08_1
# input labels, find job category and create set of jobs
index = np.where(labels == 'ISCO08_1')
jobs = set(data[:,index].flatten())

# Create a numpy array per job category (ISCO08_1) and save as array
for job in jobs:
    select = np.where(data[:,index[0][0]] == job)
    np.save('full/job' + str(job) + '.npy', data[select[0]])
