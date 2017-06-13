# Sorts data by job categorie.

import numpy as np
import sklearn as sk
import generateData as gd

(labels, data) = gd.getData()

# Jobs are in ISCO08_1

index = np.where(labels == 'ISCO08_1')
jobs = set(data[:,index].flatten())

for job in jobs:
    select = np.where(data[:,index] == job)
    np.save('full/job' + str(job) + '.npy', data[select])
