import numpy as np
from models import *

questions_total = 20
students_total = 50

log = Logs()

# initialize all students here
for i in range(0, students_total):
    log.add_student(0.7, 0.1)

# initalize one answer per question
for i in range(0, questions_total):
    log.add_answer(i, True)

# initialize an exam here
log.random_init()

# calculate score of each answer
# remember, only one answer for each question
for i in range(0, len(log.answer)):
    n_graders = 0
    score = 0.0
    for j in range(0, len(log.log)):
        if log.log[j].question_id == log.answer[i].question_id:
            s = log.student[log.log[j].student_id]
            n_graders += 1
            if log.log[j].answer_tf == True:
                score += s.reliability_mu
            else:
                score += (1-s.reliability_mu)
    log.answer[i].score = score/n_graders

# calculate score for each student based on the answers score
for i in range(0, len(log.student)):
    n_answers = 0
    score = 0.0
    for j in range(0, len(log.log)):
        if log.log[j].student_id == i:
            a = log.answer[log.log[j].question_id]
            n_answers += 1
            if log.log[j].answer_tf == True:
                score += a.score
            else:
                score += (1-a.score)
    log.student[i].score = score/n_answers

log.show(True, True)
