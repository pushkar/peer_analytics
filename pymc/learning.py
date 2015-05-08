import pymc as pm
import numpy as np
from pymc.Matplot import plot
from pylab import *
from pprint import *
import scipy.stats as stats

colors = ["#348ABD", "#A60628"]
np.set_printoptions(precision=2)

n_students = 10
n_questions = 10

def plot_artificial_dataset(n_s, n_q):
    data = np.zeros(shape=(n_s, n_q), dtype=int)
    s_scores = np.r_[pm.rdiscrete_uniform(1, 100, n_s)/100.]
    q_scores = np.r_[np.arange(0, 1, 1./n_q)]
    for si in range(0, n_s):
        for qi in range(0, n_q):
            if s_scores[si] > q_scores[qi]:
                data[si, qi] = 1

    return data

data = plot_artificial_dataset(n_students, n_questions)
print data[0, :]

x = range(0, n_questions)

score = pm.Uniform("score", 0, 1.)
observed = pm.Bernoulli("observed", score, value=data[0, :], observed=True)

model = pm.Model([score, observed])

map_ = pm.MAP(model)
map_.fit()
mcmc = pm.MCMC(model)
mcmc.sample(20000, 4000)

print "score is " + str(mcmc.stats()["score"]["mean"])

score_samples = mcmc.trace("score")[:, None]

plt.subplot(211)
plt.scatter(x, data[0, :], s=75, color="k", alpha=0.5)
plt.yticks([0, 1])
plt.ylabel("Correct/Wrong")
plt.xlabel("Question Number")
plt.title("Data")

plt.subplot(212)
plt.hist(score_samples, histtype='stepfilled', bins=35, alpha=0.85,
         label=r"posterior of score", color="#7A68A6", normed=True)
plt.legend()

show()
