import pymc as pm
from pymc.Matplot import plot
from pylab import *
from pprint import *

n = 100
p = pm.Uniform("freq_cheating", 0, 1)

answers = pm.Bernoulli("answers", p, size=n)
first = pm.Bernoulli("first", 0.5, size=n)
second = pm.Bernoulli("second", 0.5, size=n)

@pm.deterministic
def observed_answers(answers=answers, first=first, second=second):
    observed = first*answers + (1-first) * second
    return observed.sum()/float(n)

observations = pm.Binomial("observations", n, observed_answers, observed=True, value=35)

model = pm.Model([p, answers, first, second, observed_answers, observations])

mcmc = pm.MCMC(model)
mcmc.sample(40000, 10000)

trace = mcmc.trace("freq_cheating")[:]
plt.hist(trace, histtype="stepfilled", normed=True, bins=30, label="posterior", alpha=0.85, color="#348ABD")
plt.vlines([.05, .35], [0, 0], [5, 5], alpha=0.3)
plt.xlim(0, 1)
plt.legend()

show()
