import numpy as np

class Student:
    def __init__(self, reliability_mu, reliability_var):
        self.reliability_mu = reliability_mu
        self.reliability_var = reliability_var
        self.score = 0.0

class Answer:
    def __init__(self, question_id, answer_tf):
        self.score = 0.0
        self.answer_tf = answer_tf
        self.question_id = question_id

class Log:
    def __init__(self, question_id, student_id, answer_tf):
        self.question_id = question_id
        self.student_id = student_id
        self.answer_tf = answer_tf


class Logs:
    def __init__(self):
        self.student = []
        self.answer = []
        self.log = []

    def add_student(self, reliability_mu, reliability_var):
        self.student.append(Student(reliability_mu, reliability_var))
        return len(self.student)-1

    def get_student_byid(self, id):
        return self.student[id]


    def add_answer(self, question_id, answer_tf):
        self.answer.append(Answer(question_id, answer_tf))
        return len(self.answer)-1

    def get_answer_byid(self, id):
        return self.answer[id]

    def add_log(self, question_id, student_id, answer_tf):
        self.log.append(Log(question_id, student_id, answer_tf))
        return len(self.log)-1

    def get_log_byid(self, id):
        return self.log[id]

    def get_log_byid(self, student_id, question_id):
        for i in range(0, len(self.log)):
            if self.log[i].student_id == student_id and self.log[i].question_id == question_id:
                return i
        return -1

    def show(self, print_answer_score=False, print_student_score=False):
        print "Log Data:"
        for i in range(0, len(self.answer)):
            print '\tQ' + str(i),
        print ''

        for i in range(0, len(self.student)):
            print 'S' + str(i),
            for j in range(0, len(self.answer)):
                log_id = self.get_log_byid(i, j)
                if log_id >= 0:
                    if self.log[log_id].answer_tf == True:
                        print '\t' + str(1),
                    else:
                        print '\t' + str(0),
                else:
                    print '\t' + 'null',

            if print_student_score == True:
                print '\t' + str(self.student[i].reliability_mu), str(self.student[i].score),
            print ''

        if print_answer_score == True:
            for j in range(0, len(self.answer)):
                print '\t' + str(self.answer[j].score),

        print "\n"

    def random_init(self):
        for i in range(0, len(self.student)):
            s = self.student[i]
            for j in range(0, len(self.answer)):
                rand = np.random.normal(s.reliability_mu, s.reliability_var, 1)
                tf = False
                if rand[0] > 0.5:
                    tf = True
                self.add_log(j, i, tf)
                
    def test(self):
        print "This is a test"
