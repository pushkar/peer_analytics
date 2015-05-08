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

def gen_artificial_dataset(n_s, n_q):
    data = np.zeros(shape=(n_s, n_q), dtype=int)
    s_scores = np.r_[pm.rdiscrete_uniform(1, 100, n_s)/100.]
    q_scores = np.r_[np.arange(0, 1, 1./n_q)]
    for si in range(0, n_s):
        for qi in range(0, n_q):
            if s_scores[si] > q_scores[qi]:
                data[si, qi] = 1

    return data

data = gen_artificial_dataset(n_students, n_questions)

# student scores, question hardness
students = np.empty(n_students, dtype=object)
questions = np.empty(n_questions, dtype=object)

observed = np.empty(n_students, dtype=object)

for i in range(0, n_students):
    students[i] = pm.Uniform('score_%i' % i, 0, 1.)
    observed[i] = pm.Bernoulli('observed_%i' % i, students[i], value=data[i, :], observed=True)

for i in range(0, n_questions):
    questions[i] = pm.Uniform('question_%i' % i, 0, 1.)

model = pm.Model(np.r_[students, observed])

map_ = pm.MAP(model)
map_.fit()
mcmc = pm.MCMC(model)
mcmc.sample(20000, 4000)

print data

for i in range(0, n_students):
    score_samples = mcmc.trace('score_%i'%i)[:]
    print "score for student " + str(i) + " is " + str(score_samples.mean())
