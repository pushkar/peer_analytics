import pymc as pm
from numpy import *
from pymc.Matplot import plot
from pylab import *
from pprint import *

p_a = pm.Uniform('p_a', lower=0, upper=1)
p_b = pm.Uniform('p_b', lower=0, upper=1)

p_a_true = 0.05
p_b_true = 0.04
n_a = 1000
n_b = 2000

obs_a = pm.rbernoulli(p_a_true, n_a)
obs_b = pm.rbernoulli(p_b_true, n_b)

obs_A = pm.Bernoulli("obs_A", p_a, value=obs_a, observed=True)
obs_B = pm.Bernoulli("obs_B", p_b, value=obs_b, observed=True)

@pm.deterministic
def delta(p_a=p_a, p_b=p_b):
    return p_a - p_b

mcmc = pm.MCMC([p_a, p_b, delta, obs_A, obs_B])
mcmc.sample(18000, 100)

p_a_samples = mcmc.trace("p_a")[:]
p_b_samples = mcmc.trace("p_b")[:]
delta_samples = mcmc.trace("delta")[:]

ax = plt.subplot(311)

plt.title("Posterior of $p_a$, $p_b$ and delta")

plt.xlim(0, .1)
plt.vlines(p_a_true, 0, 90, linestyle="--", label="true $p_a$ (unknown)")
plt.hist(p_a_samples, bins=25, histtype="stepfilled", normed=True, color="#A60628", label="posterior of $p_a$")
plt.legend()

ax = plt.subplot(312)
plt.xlim(0, .1)
plt.vlines(p_b_true, 0, 90, linestyle="--", label="true $p_b$ (unknown)")
plt.hist(p_b_samples, bins=25, histtype="stepfilled", normed=True, color="#467821", label="posterior of $p_b$")
plt.legend()

ax = plt.subplot(313)
plt.xlim(0, .1)
plt.vlines(p_a_true-p_b_true, 0, 90, linestyle="--", label="true delta (unknown)")
plt.hist(delta_samples, bins=25, histtype="stepfilled", normed=True, color="#7A68A6", label="posterior of delta")
plt.legend()

plt.show()
