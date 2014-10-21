import numpy as np

class Student:
    def __init__(self, id):
        self.reliability = 0.7
        self.score = 0.0
        self.id = id

class Answer:
    def __init__(self, question_id):
        self.score = 0.0
        self.answer_tf = True # this is the correct answer
        self.question_id = question_id

class Log:
    def __init__(self, question_id, student_id, answer_tf):
        self.question_id = question_id
        self.student_id = student_id
        self.answer_tf = answer_tf

questions_total = 20
students_total = 50

log = []
student = []
answer = []

def get_log_byid(student_id, question_id):
    for i in range(0, len(log)):
        if log[i].student_id == student_id and log[i].question_id == question_id:
            return i
    return -1

def print_log(print_answer_score=False, print_student_score=False):
    print "Log Data:"
    for i in range(0, questions_total):
        print '\tQ' + str(i),
    print ''

    for i in range(0, students_total):
        print 'S' + str(i),
        for j in range(0, questions_total):
            log_id = get_log_byid(i, j)
            if log_id >= 0:
                if log[log_id].answer_tf == True:
                    print '\t' + str(1),
                else:
                    print '\t' + str(0),
            else:
                print '\t' + 'null',

        if print_student_score == True:
            print '\t' + str(student[i].reliability), str(student[i].score),
        print ''

    if print_answer_score == True:
        for j in range(0, questions_total):
            print '\t' + str(answer[j].score),

    print "\n"


# initialize all students here
for i in range(0, students_total):
    student.append(Student(i))

# initalize one answer per question
for i in range(0, questions_total):
    answer.append(Answer(i))

print 'There are ' + str(len(student)) + ' students'

# initialize an exam here, this happens in Log
# all students grade one answer for each question
# correct answer of all questions is always True
for i in range(0, students_total):
    s = student[i]
    for j in range(0, questions_total):
        rand = np.random.normal(s.reliability, 0.2, 1)
        tf = False
        if rand[0] > 0.5:
            tf = True
        log.append(Log(j, i, tf))

print 'There are ' + str(len(answer)) + ' answers'
print 'There are ' + str(len(log)) + ' logs\n'

# calculate score of each answer
# remember, only one answer for each question
for i in range(0, len(answer)):
    n_graders = 0
    score = 0.0
    for j in range(0, len(log)):
        if log[j].question_id == answer[i].question_id:
            s = student[log[j].student_id]
            n_graders += 1
            if log[j].answer_tf == True:
                score += s.reliability
            else:
                score += (1-s.reliability)
    answer[i].score = score/n_graders

# calculate score for each student based on the answers score
for i in range(0, len(student)):
    n_answers = 0
    score = 0.0
    for j in range(0, len(log)):
        if log[j].student_id == student[i].id:
            a = answer[log[j].question_id]
            n_answers += 1
            if log[j].answer_tf == True:
                score += a.score
            else:
                score += (1-a.score)
    student[i].score = score/n_answers

print_log(True, True)
