import pymc as pm
import numpy as np
from pymc.Matplot import plot
from pylab import *
from pprint import *
import scipy.stats as stats

colors = ["#348ABD", "#A60628"]
np.set_printoptions(precision=2)

# Number of students and submissions
n = 5
n_graders = 3

def plot_artificial_dataset(n):
    data = np.zeros(shape=(n, n), dtype=float)
    #reliability = np.r_[pm.rdiscrete_uniform(1, 100, n)/100.]
    true_score = np.r_[pm.rdiscrete_uniform(1, 5, n)]
    for i in range(0, n):
        for j in np.random.choice(range(0, n), n_graders):
            data[i, j] = int(pm.rnormal(true_score[i], 10)) #1./reliability[j])

    return data

data = plot_artificial_dataset(n)
print data

# reliability, true scores and observed scores
r = np.empty(n, dtype=object)
s = np.empty(n, dtype=object)
o = np.empty(n*n, dtype=object)

for i in range(0, n):
    r[i] = pm.Gamma('r_%i' % i, 1, 0.01)
    s[i] = pm.Normal('s_%i' % i, 0, 0.1)

for i in range(0, n): #user
    for j in range(0, n): #assignment
        if fabs(data[j, i]) > 1e-6:
            o[i*n+j] = pm.Normal('o_%i%i' % (i, j), s[j], 1./r[i], value=data[j, i], observed=True)

model = pm.Model(np.r_[r, s, o])
#map_ = pm.MAP(model)
#map_.fit()
mcmc = pm.MCMC(model)
mcmc.sample(12000, 2000, 2)

pprint(mcmc.stats())
x = np.linspace(0, 5, 100)

for i in range(0, n):
    figure(i)
    r_samples = mcmc.trace('r_%i'%i)[:]
    s_samples = mcmc.trace('s_%i'%i)[:]
    s_y = stats.norm.pdf(x, s_samples.mean(), s_samples.std())

    d = data[i, :]
    if size(d[(d > 0)]) < 1:
        pass

    ax = plt.subplot(311)
    plt.xlim(0, 5)
    plt.hist(d[(d > 0)], bins=n_graders, histtype="stepfilled", label="observed")
    plt.legend()

    ax = plt.subplot(312)
    plt.hist(r_samples, bins=25, histtype="stepfilled", normed=True, color="#A60628", label="$r$ = %.2f" % r_samples.mean())
    plt.legend()

    ax = plt.subplot(313)
    plt.xlim(0, 5.)
    plt.hist(s_samples, bins=100, histtype="stepfilled", normed=True, color="#20B2AA", label="$s$ = %.2f" % s_samples.mean())
    plt.plot(x, s_y, color="#000000", lw=1)
    plt.fill_between(x, s_y, color=colors[0], alpha=0.3)
    plt.legend()

show()
