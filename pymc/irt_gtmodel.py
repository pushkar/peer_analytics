import pymc as pm
import numpy as np
from pymc.Matplot import plot
from pylab import *
from pprint import *
import scipy.stats as stats
import itertools
import random

colors = ["#348ABD", "#A60628"]
np.set_printoptions(precision=2)

#db = pm.database.pickle.load('irt.pickle')

n_students = 10
n_questions =  10
n_questions_per_exam = 3

def gen_artificial_dataset(n_s, n_q):
    x = np.arange(0, n_q, 1)
    data = np.zeros(shape=(n_s, n_q), dtype=int)

    s_scores = np.r_[pm.rdiscrete_uniform(1, n_s*10, n_s)/10.]
    q_scores = np.r_[pm.rdiscrete_uniform(1, n_q*10, n_q)/10.]
    s_scores.sort()
    q_scores.sort()

    #s_scores = np.r_[np.arange(0.1, n_students+0.1, 1.)]
    #q_scores = np.r_[np.arange(0.1, n_questions+0.1, 1.)]

    for si in range(0, n_s):
        for qi in random.sample(range(0, n_q), n_questions_per_exam):
            if s_scores[si] >= q_scores[qi]:
                data[si, qi] = 1
            else:
                data[si, qi] = -1

    return data, x, s_scores, q_scores

def all_pairs(lst):
    for p in itertools.permutations(lst):
        i = iter(p)
        yield zip(i,i)

def sigmoid(s, q):
    return (1. / (1. + np.exp(-s+q)))

data, x, s_scores, q_scores = gen_artificial_dataset(n_students, n_questions)
print "Student Proficiency is " + str(s_scores)
print "Question Proficiency is " + str(q_scores)
print "----\n"

punish = 1. # how much to punish, possibly redundant
i = 5 # student number
n_pick = 2 # number of questions to pick

# Find the questions that student can answer correctly/incorrectly
questions = {}

print "Student's proficiency: " + str(s_scores[i])

for j in range(0, n_questions):
    q_stat = {}
    if data[i, j] < 1:
        p = sigmoid(s_scores[i], q_scores[j])
        h = q_scores[j]# - s_scores[i]
        q_stat["diff"] = round(h, 2)
        q_stat["p"] = round(p, 2)

        if h <= 0:
            r_correct = 1.
            r_incorrect = -1*punish
        else:
            r_correct = punish
            r_incorrect = -1.

        a_c = abs(h)*r_correct
        a_ic = abs(h)*r_incorrect
        a_c = 0.5*np.exp(0.5*h)*r_correct
        a_ic = a_c*r_incorrect

        q_stat["c_c"] = round(a_c, 2)
        q_stat["c_i"] = round(a_ic, 2)


        q_stat["c_payoff"] = round( (p*a_c) + ((1.-p)*a_ic), 2)

        questions[j] = q_stat

pprint(questions)
print ""
