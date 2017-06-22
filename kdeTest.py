"""
===================================
Simple 1D Kernel Density Estimation
===================================
This example uses the :class:`sklearn.neighbors.KernelDensity` class to
demonstrate the principles of Kernel Density Estimation in one dimension.

The first plot shows one of the problems with using histograms to visualize
the density of points in 1D. Intuitively, a histogram can be thought of as a
scheme in which a unit "block" is stacked above each point on a regular grid.
As the top two panels show, however, the choice of gridding for these blocks
can lead to wildly divergent ideas about the underlying shape of the density
distribution.  If we instead center each block on the point it represents, we
get the estimate shown in the bottom left panel.  This is a kernel density
estimation with a "top hat" kernel.  This idea can be generalized to other
kernel shapes: the bottom-right panel of the first figure shows a Gaussian
kernel density estimate over the same distribution.

Scikit-learn implements efficient kernel density estimation using either
a Ball Tree or KD Tree structure, through the
:class:`sklearn.neighbors.KernelDensity` estimator.  The available kernels
are shown in the second figure of this example.

The third figure compares kernel density estimates for a distribution of 100
samples in 1 dimension.  Though this example uses 1D distributions, kernel
density estimation is easily and efficiently extensible to higher dimensions
as well.
"""
# Author: Jake Vanderplas <jakevdp@cs.washington.edu>
#
import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import norm
from sklearn.neighbors import KernelDensity
import storyData as sd
import sortByLabel as sbl
TARGET = 'ISCO08_1'

labels, cleanCatData = sd.getCatData()
targetColumnNr = np.where(labels == TARGET)[0][0]
# fill iq scores for better training
# storiesData = sd.fillStoryIq(TARGET, labels, cleanCatData)

catArrays, storyLabels = sbl.splitForStory(TARGET, labels, cleanCatData)

#----------------------------------------------------------------------
# Plot the progression of histograms to kernels
np.random.seed(1)
N = 20
CAT = 2
FEATURE = 14
X_raw = catArrays[CAT][:,FEATURE].reshape(catArrays[CAT].shape[0], 1)
delIdx = np.where(X_raw == -1.)
X = np.delete(X_raw, delIdx[0], 0)

# X = np.concatenate((np.random.normal(0, 1, int(0.3 * N)),
#                     np.random.normal(5, 1, int(0.7 * N))))[:, np.newaxis]

print X.shape
print X
X_plot = np.linspace(0, 100, 101)[:, np.newaxis]
bins = np.linspace(0, 10, 11)

fig, ax = plt.subplots(2, 2, sharex=True, sharey=True)
fig.subplots_adjust(hspace=0.05, wspace=0.05)

# histogram 1
ax[0, 0].hist(X[:, 0], bins=bins, fc='#AAAAFF')#, normed=True)
ax[0, 0].text(-3.5, 0.31, "Histogram")

# histogram 2
ax[0, 1].hist(X[:, 0], bins=bins + 0.75, fc='#AAAAFF')#, normed=True)
ax[0, 1].text(-3.5, 0.31, "Histogram, bins shifted")

# tophat KDE
kde = KernelDensity(kernel='tophat', bandwidth=0.75).fit(X)
log_dens = kde.score_samples(X_plot)
ax[1, 0].fill(X_plot[:, 0], np.exp(log_dens), fc='#AAAAFF')
ax[1, 0].text(-3.5, 0.31, "Tophat Kernel Density")

# Gaussian KDE
kde = KernelDensity(kernel='gaussian', bandwidth=0.75).fit(X)
log_dens = kde.score_samples(X_plot)
ax[1, 1].fill(X_plot[:, 0], np.exp(log_dens), fc='#AAAAFF')
ax[1, 1].text(-3.5, 0.31, "Gaussian Kernel Density")

for axi in ax.ravel():
    axi.plot(X[:, 0], np.zeros(X.shape[0]) - 0.01, '+k')
    axi.set_xlim(0, 100)
    axi.set_ylim(0, .1)

for axi in ax[:, 0]:
    axi.set_ylabel('Normalized Density')

for axi in ax[1, :]:
    axi.set_xlabel('x')


plt.show()
import pandas as pd
import numpy as np
import scipy.stats as stats
import matplotlib.pyplot as plt

np.random.seed(0)
gaussian1 = -6 + 3 * np.random.randn(1700)
gaussian2 = 4 + 1.5 * np.random.randn(300)
gaussian_mixture = np.hstack([gaussian1, gaussian2])

df = pd.DataFrame(gaussian_mixture, columns=['data'])

# non-parametric pdf
nparam_density = stats.kde.gaussian_kde(df.values.ravel())
x = np.linspace(-20, 10, 200)
nparam_density = nparam_density(x)

# parametric fit: assume normal distribution
loc_param, scale_param = stats.norm.fit(df)
param_density = stats.norm.pdf(x, loc=loc_param, scale=scale_param)

fig, ax = plt.subplots(figsize=(10, 6))
ax.hist(df.values, bins=30, normed=True)
ax.plot(x, nparam_density, 'r-', label='non-parametric density (smoothed by Gaussian kernel)')
ax.plot(x, param_density, 'k--', label='parametric density')
ax.set_ylim([0, 0.15])
ax.legend(loc='best')
