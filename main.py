from flask import Flask, render_template
import numpy, random

teachers = ['S','SG','GS','AM','HP','VB','AA','BS','ND']
teacher_count = -1

classes = {
    'FYIT' : ['OOP', 'DBMS','WP',   'DM',  'TOLS', 'PP'],
    'FYCS' : ['WP',  'DM',  'TOLS', 'DBMS','OOP',  'PP'],
    'SYIT' : ['SE',  'ES',  'CG',   'CJ',  'COST'],
    'SYCS' : ['CN', 'LA',  'FA',   'ADF', 'NET',  'AJ', 'SE'],
    'TYIT' : ['ITSM','SC',  'BI',   'AMP', 'SQM',  'PGIS'],
    'TYCS' : ['EH',  'CC',  'DIP',  'DS']
}

classes_map = ['FYIT','FYCS','SYIT','SYCS','TYIT','TYCS']

def assign_teacher():
    '''assigns subjects to teachers evenly'''
    global teacher_count
    teacher_count = (teacher_count + 1) % len(teachers)
    return teachers[teacher_count]


class Subject:
    def __init__(self, name, CLASS, teacher, TYPE = 'normal'):
        self.name = name
        self.CLASS = CLASS
        self.id = classes_map.index(CLASS)
        self.teacher = teacher
        if self.id % 2 == 0: self.start_time = 0
        else: self.start_time = 2
        if TYPE == 'normal': self.count, self.value, self.colour = 3, 1, 'white'
        else: self.count, self.value, self.colour = 1, 2, 'yellow'
        self.running_behind = 0


class Class:
    def __init__(self, name):
        self.name = name
        self.SUBJECTS = []  
        self.PRAC_SUBJECTS = []

    def add_subject(self, subject):
        ''' add a normal subject'''
        self.SUBJECTS.append(subject)

    def add_prac_subject(self, subject):
        ''' add a practical subject'''
        self.PRAC_SUBJECTS.append(subject)


class Department:
    def __init__(self, name):
        self.name = name
        self.CLASSES = []
        self.LABS = 3
        self.CLASSROOMS = 6

    def add_class(self, CLASS):
        ''' add a class '''
        self.CLASSES.append(CLASS)

    def display_class_subjects(self):
        ''' displays class-wise subject names, can be modified '''
        for CLASS in self.CLASSES:
            print(CLASS.name, end = ':\t')
            for SUBJECT in CLASS.PRAC_SUBJECTS + CLASS.SUBJECTS:
                print(SUBJECT.name, end = ', ')
                #print(SUBJECT.teacher, end = ', ')
            print('\n')


class TT:
    def __init__(self, DEPARTMENT):
        self.DEPT = DEPARTMENT
        self.grid = numpy.zeros((6,6,8), dtype = Subject)
        self.PRAC_SUBJECTS, self.NORMAL_SUBJECTS = self.sort_subjects()

        total_count, valid = self.total_count()
        print(total_count)
        if not valid:
            print('Count should be less than 36 for each class')

        self.assign_pracs()
        self.assign_normal()
        
    def sort_subjects(self):
        ''' separates normal and practical lectures '''
        NORMAL_SUBJECTS, PRAC_SUBJECTS = [], []
        for CLASS in self.DEPT.CLASSES:
            for SUBJECT in CLASS.SUBJECTS:
                NORMAL_SUBJECTS.append(SUBJECT)
            for PRAC in CLASS.PRAC_SUBJECTS:
                PRAC_SUBJECTS.append(PRAC)
        return PRAC_SUBJECTS, NORMAL_SUBJECTS

    def assign_pracs(self):
        ''' schedules practical lectures in the TT '''
        random.shuffle(self.PRAC_SUBJECTS)
        day, subject = 0, 0
        while self.PRAC_SUBJECTS != []:
            clss, time = self.PRAC_SUBJECTS[subject].id, self.PRAC_SUBJECTS[subject].start_time
            while True:
                #print(clss, day, time)
                if self.grid[clss][day][time] == 0:    
                    if self.check_availability(self.PRAC_SUBJECTS[subject], day, time, self.DEPT.LABS):
                        if (time < 8) and (self.grid[clss][day][time + 1] == 0):
                            if (self.check_availability(self.PRAC_SUBJECTS[subject], day, time + 1, self.DEPT.LABS)):
                                self.grid[clss][day][time], self.grid[clss][day][time + 1] = [self.PRAC_SUBJECTS[subject]] * 2
                                self.PRAC_SUBJECTS.remove(self.PRAC_SUBJECTS[subject])
                                break
                day += 1
                if day > 5:
                    time += 1
                    if time > self.PRAC_SUBJECTS[subject].start_time + 6: time = 0                     
                    day = 0

    def assign_normal(self):
        ''' schedules normal lectures in the TT '''
        random.shuffle(self.NORMAL_SUBJECTS)

        day, subject = 0, 0
        while self.NORMAL_SUBJECTS != []:
            clss, time = self.NORMAL_SUBJECTS[subject].id, self.NORMAL_SUBJECTS[subject].start_time
            while True:
                #print(clss, day, time)
                if self.grid[clss][day][time] == 0:    
                    if self.check_availability(self.NORMAL_SUBJECTS[subject], day, time, self.DEPT.CLASSROOMS):
                        self.grid[clss][day][time] = self.NORMAL_SUBJECTS[subject]
                        self.NORMAL_SUBJECTS[subject].count -= 1
                        if self.NORMAL_SUBJECTS[subject].count + self.NORMAL_SUBJECTS[subject].running_behind < 1: self.NORMAL_SUBJECTS.remove(self.NORMAL_SUBJECTS[subject])
                        break
                day += 1
                if day > 5:
                    time += 1
                    if time >= self.NORMAL_SUBJECTS[subject].start_time + 6: time = 0                     
                    day = 0

    def check_availability(self, subject, y, z, ROOM_COUNT):
        ''' checks for available classrooms/labs, and for teacher availability '''
        rooms = 0
        for n in range(len(self.grid)):
            if self.grid[n][y][z] != 0:
                if (rooms >= ROOM_COUNT) or (self.grid[n][y][z].teacher == subject.teacher):
                    return False
                rooms += 1
        return True

    def display_grid(self):
        ''' displays TT cmd '''
        for i in range(len(self.grid)):
            for j in range(len(self.grid[i])):
                print('-------------------------------------------------------------------')
                for k in range(len(self.grid[i][j])):
                    if self.grid[i][j][k] == 0:
                        print('',0, end = '\t')
                        continue
                    print('',self.grid[i][j][k].name, end = '\t')
                print()
            print('-------------------------------------------------------------------\n\n')

    def total_count(self):
        count = []; valid = True
        for clss in self.DEPT.CLASSES:
            sub_count = 0
            for sub in clss.SUBJECTS + clss.PRAC_SUBJECTS:
                sub_count += sub.count * sub.value
            if sub_count > 36:
                valid = False
                break
            count.append(sub_count)
        return count, valid

    def calculate_fitness(self):
        ''' closeness towards ideal, 0 is good '''
        total = [0 for i in range(len(self.grid))]
        for _class in range(len(self.grid)):
            for day in self.grid[_class]:
                start = False; counter = 0; i = 0
                for k in range(len(day)):
                    if not start:
                        if day[k] != 0:
                            start = True
                    elif day[k] == 0:
                        counter += 1
                    else:
                        total[_class] += counter
                        counter = 0
        return total


app = Flask('my_app')

@app.route('/')
def main():
    D = Department('IT/CS')
    ''' Input data '''
    for CLASS in classes:
        C = Class(CLASS)
        for subject in classes[CLASS]:
            teacher = assign_teacher()
            S = Subject(subject, C.name, teacher)
            C.add_subject(S)
            if S.name != 'SE': #se no prac
                P = Subject(subject + ' P', C.name, teacher, TYPE = 'prac')
                C.add_prac_subject(P)
        D.add_class(C)
    #D.display_class_subjects()
    #print(D.CLASSES[2].SUBJECTS[0].name)

    ''' setting extra lectures '''
    D.CLASSES[2].SUBJECTS[0].running_behind += 2 #SE
    D.CLASSES[3].SUBJECTS[0].running_behind += 4 #CN
    D.CLASSES[3].SUBJECTS[1].running_behind -= 3 #LA
    
    T = TT(D)
    #print([i.name for i in T.NORMAL_SUBJECTS])
    #print([i.name for i in T.PRAC_SUBJECTS])

    #T.display_grid()
    fitness = T.calculate_fitness()

    data = {'tt': T.grid, 'fitness': fitness}

    return render_template('main.html', data = data)

if __name__ == '__main__':
    app.run(debug = True, port = 5000)



'''
70 total, 35 * 3 + 35 * 2 = 175 total lectures per week / 6 = 29 per class avg / 6 days = 5 lectures per day avg.
1. Assign prac lectures for all classes, evenly
'''