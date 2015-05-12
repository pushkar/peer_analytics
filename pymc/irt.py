import pymc as pm
import numpy as np
from pymc.Matplot import plot
from pylab import *
from pprint import *
import scipy.stats as stats

colors = ["#348ABD", "#A60628"]
np.set_printoptions(precision=2)

n_students = 1
n_questions = 10

def gen_artificial_dataset(n_s, n_q):
    x = np.arange(0, n_q, 1)
    data = np.zeros(shape=(n_s, n_q), dtype=int)
    s_scores = np.r_[pm.rdiscrete_uniform(1, 100, n_s)/100.]
    q_scores = np.r_[np.arange(0.1, 1.1, 1./n_q)]
    for si in range(0, n_s):
        for qi in range(0, n_q):
            if s_scores[si] > q_scores[qi]:
                data[si, qi] = 1

    return data, x, s_scores, q_scores

data, x, s_scores, q_scores = gen_artificial_dataset(n_students, n_questions)

print "Student Proficiency is " + str(s_scores)
y = data[0,:]
print x, y

proficiency = pm.Normal("prof", 0, 0.01, value = 0)
hardness = pm.Normal("hardness", 0, 0.01, value = 0)

@pm.deterministic
def p(x=x, p=proficiency, h=hardness):
    return 1.0/(1. + np.exp(p*x + h))

observed = pm.Bernoulli("observed", p, value=y, observed=True)

model = pm.Model([proficiency, hardness, observed])
map_ = pm.MAP(model)
map_.fit()
mcmc = pm.MCMC(model)
mcmc.sample(12000, 4000, 2)

proficiency_samples = mcmc.trace("prof")[:, None]
hardness_samples = mcmc.trace("hardness")[:, None]

print mcmc.stats()["prof"]["mean"]
print mcmc.stats()["hardness"]["mean"]

def logistic(x, beta, alpha=0):
    return 1.0 / (1.0 + np.exp(np.dot(beta, x) + alpha))

x_ = np.linspace(0, 10, 200)

plt.subplot(311)
plt.scatter(x, y, s=75, color="k", alpha=0.5)
plt.yticks([0, 1])
plt.plot(x_, logistic(x_, mcmc.stats()["prof"]["mean"], mcmc.stats()["hardness"]["mean"]), color="#348ABD")
plt.ylabel("Prof")
plt.xlabel("Questiom")
plt.title("IRT")

plt.subplot(312)
plt.hist(proficiency_samples, histtype='stepfilled', bins=35, alpha=0.85,
         label=r"posterior of prof", color="#7A68A6", normed=True)
plt.legend()

plt.subplot(313)
plt.hist(hardness_samples, histtype='stepfilled', bins=35, alpha=0.85,
         label=r"posterior of hard", color="#A60628", normed=True)
plt.legend();

show()
