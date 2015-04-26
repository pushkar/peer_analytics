import pymc as pm
import numpy as np
from pymc.Matplot import plot
from pylab import *
from pprint import *

n = 100
s_true = 2.5

data = np.r_[pm.rnormal(s_true, 0.1, n)]
print data

# reliability, true scores and observed scores
r = pm.Gamma("r", 1, 0.01)
s = pm.Normal("s", 0, 0.1)
o = pm.Normal("o", s, 1./r, value=data, observed=True)

model = pm.Model([r, s, o])
mcmc = pm.MCMC(model)
mcmc.sample(12000, 2000, 2)

pprint(mcmc.stats())

r_samples = mcmc.trace("r")[:]
s_samples = mcmc.trace("s")[:]

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
