import pymc as pm
import numpy as np
from pymc.Matplot import plot
from pylab import *
from pprint import *


# Number of students and submissions
n = 5

def plot_artificial_dataset(n):
    data = np.zeros(shape=(n, n), dtype=float)
    #reliability = np.r_[pm.rdiscrete_uniform(1, 100, n)/100.]
    true_score = np.r_[pm.rdiscrete_uniform(0, 5, n)]
    for i in range(0, n):
        for j in range(0, n):
            data[i, j] = pm.rnormal(true_score[i], 10) #1./reliability[j])

    # print "Reliability scores:"
    # print reliability
    # print "True Scores"
    # print true_score
    # print "Observed Scores"
    # print data

    return data

data = plot_artificial_dataset(10)

print data

# reliability, true scores and observed scores
r = np.empty(n, dtype=object)
s = np.empty(n, dtype=object)
o = np.empty(n*n, dtype=object)

for i in range(0, n):
    r[i] = pm.Gamma('r_%i' % i, 1, 0.01)
    s[i] = pm.Normal('s_%i' % i, 0, 0.1)
    for j in range(0, n):
        o[i*n+j] = pm.Normal('o_%i%i' % (i, j), s[j], 1./r[i], value=data[:, j], observed=True)

model = pm.Model(np.r_[r, s, o])
mcmc = pm.MCMC(model)
mcmc.sample(12000, 2000, 2)

pprint(mcmc.stats())

for i in range(0, n):
    figure(i)
    r_samples = mcmc.trace('r_%i'%i)[:]
    s_samples = mcmc.trace('s_%i'%i)[:]

    ax = plt.subplot(311)
    plt.xlim(0, 5.)
    plt.hist(data, bins=25, histtype="stepfilled", normed=True, label="observed")
    plt.legend()

    ax = plt.subplot(312)
    plt.hist(r_samples, bins=25, histtype="stepfilled", normed=True, color="#A60628", label="posterior of $r$")
    plt.legend()

    ax = plt.subplot(313)
    plt.xlim(0, 5.)
    plt.hist(s_samples, bins=25, histtype="stepfilled", normed=True, color="#467821", label="posterior of $s$")
    plt.legend()

show()
