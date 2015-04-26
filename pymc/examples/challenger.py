import pymc as pm
import numpy as np
from pymc.Matplot import plot
from pylab import *

np.set_printoptions(precision=3, suppress=True)
challenger_data = np.genfromtxt("challenger_data.csv", skip_header=1,
                                usecols=[1, 3], missing_values="NA",
                                delimiter=",")

challenger_data = challenger_data[~np.isnan(challenger_data[:, 1])]

n = size(challenger_data[:, 1])
for i in linspace(1, n-1, n-1):
    if challenger_data[i, 1] > 0:
        challenger_data[i, 1] = 1


temperature = challenger_data[:, 0]
defect = challenger_data[:, 1]

alpha = pm.Normal("alpha", 0, 0.001, value=0)
beta = pm.Normal("beta", 0, 0.001, value=0)

@pm.deterministic
def p(t=temperature, alpha=alpha, beta=beta):
    return 1.0 / (1. + np.exp(beta * t + alpha))

observed = pm.Bernoulli("bernoulli_obs", p, value=defect, observed=True)

model = pm.Model([observed, alpha, beta])

map_ = pm.MAP(model)
map_.fit()
mcmc = pm.MCMC(model)
mcmc.sample(12000, 2000, 2)

alpha_samples = mcmc.trace("alpha")[:, None]
beta_samples = mcmc.trace("beta")[:, None]

def logistic(x, beta, alpha=0):
    return 1.0 / (1.0 + np.exp(np.dot(beta, x) + alpha))

x = np.linspace(5, 100, 200)


plt.subplot(311)
plt.scatter(challenger_data[:, 0], challenger_data[:, 1], s=75, color="k", alpha=0.5)
plt.yticks([0, 1])
plt.plot(x, logistic(x, mcmc.stats()["beta"]["mean"], mcmc.stats()["alpha"]["mean"]), label=r"$\beta = 1, \alpha = 1$", color="#348ABD")
plt.ylabel("Damage Incident?")
plt.xlabel("Outside Temperature")
plt.title("Challenger: Space shuttle O-Ring defect vs Temperature")

plt.subplot(312)
plt.title(r"Posterior for $\alpha$ and $\beta$")
plt.hist(beta_samples, histtype='stepfilled', bins=35, alpha=0.85,
         label=r"posterior of $\beta$", color="#7A68A6", normed=True)
plt.legend()

plt.subplot(313)
plt.hist(alpha_samples, histtype='stepfilled', bins=35, alpha=0.85,
         label=r"posterior of $\alpha$", color="#A60628", normed=True)
plt.legend();

show()
