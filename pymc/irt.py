import pymc as pm
import numpy as np
from pymc.Matplot import plot
from pylab import *
from pprint import *
import scipy.stats as stats

colors = ["#348ABD", "#A60628"]
np.set_printoptions(precision=2)

n_students = 5
n_questions = 5

def gen_artificial_dataset(n_s, n_q):
    x = np.arange(0, n_q, 1)
    data = np.zeros(shape=(n_s, n_q), dtype=int)

    s_scores = np.r_[pm.rdiscrete_uniform(1, 100, n_s)/100.]
    q_scores = np.r_[pm.rdiscrete_uniform(1, 100, n_q)/100.]

    #s_scores = np.r_[np.arange(0.1, 1.1, 1./n_s)]
    #q_scores = np.r_[np.arange(0.1, 1.1, 1./n_q)]

    for si in range(0, n_s):
        for qi in range(0, n_q):
            if s_scores[si] >= q_scores[qi]:
                data[si, qi] = 1

    return data, x, s_scores, q_scores

data, x, s_scores, q_scores = gen_artificial_dataset(n_students, n_questions)
print "Student Proficiency is " + str(s_scores)
print "Question Proficiency is " + str(q_scores)

s = np.empty(n_students, dtype=object)
for i in range(0, n_students):
    s[i] = pm.Normal('s_%i'%i, mu=0., tau=1.)

q = np.empty(n_questions, dtype=object)
for i in range(0, n_questions):
    q[i] = pm.Normal('q_%i'%i, mu=0., tau=1.)

@pm.potential
def p(data=data, s=s, q=q):
    sum = 0
    for i in range(1, n_students):
        for j in range(1, n_questions):
            r = data[i, j]
            sum -= np.log(1.0 + np.exp(-s[i]+q[j]))
            sum -= (1 - r)*(s[i]-q[j])

    for i in range(1, n_students):
        sum -= 0.5*s[i]**2

    for j in range(1, n_questions):
        sum -= 0.5*q[j]**2

    return sum


model = pm.Model(np.r_[s, q], p)
map_ = pm.MAP(model)
map_.fit()
mcmc = pm.MCMC(model)
mcmc.sample(50000, 18000)

print "Student Proficiency:"
for i in range(0, n_students):
    print mcmc.stats()["s_%i"%i]["mean"]

print "Question Hardness:"
for i in range(0, n_students):
    print mcmc.stats()["q_%i"%i]["mean"]

data_n = np.zeros(shape=(n_students, n_questions), dtype=int)
for si in range(0, n_students):
    for qi in range(0, n_questions):
        if mcmc.stats()["s_%i"%si]["mean"] >= mcmc.stats()["q_%i"%qi]["mean"]:
            data_n[si, qi] = 1
print data
print data_n
print logical_xor(data, data_n)
