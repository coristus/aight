import numpy as np
import sklearn as sk
import generateData as gd
import sortByLabel as sbl

(labels, data) = gd.getData()

catArrays, catLabels = sbl.splitByLabel('ISCO08_1', labels, data)
print catLabels[6]
print catArrays[6]
