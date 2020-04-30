from flask import Flask, render_template, redirect
from flask_bootstrap import Bootstrap
from data import teachers, teacher_count, classes_map, classes
from tt import Department, Class, Subject, TT, assign_teacher
import pickle


app = Flask('my_app')
Bootstrap(app)

@app.route('/')
def main():
    try:
        file = open('savefile.p', 'rb')
        saved_tt = pickle.load(file)
        data = {'tt': saved_tt}
    except:
        data = None
    return render_template('main.html', data = data)
    
@app.route('/create')
def create():
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

    ''' setting extra lectures '''
    '''D.CLASSES[2].SUBJECTS[0].running_behind += 2 #SE
    D.CLASSES[3].SUBJECTS[0].running_behind += 4 #CN
    D.CLASSES[3].SUBJECTS[1].running_behind -= 3 #LA'''

    T = TT(D)
    T.save_to_file()
    #x.display_grid()
    
    return redirect('/')


if __name__ == '__main__':
    app.run(debug = True, port = 5000)



'''
70 total, 35 * 3 + 35 * 2 = 175 total lectures per week / 6 = 29 per class avg / 6 days = 5 lectures per day avg.
1. Assign prac lectures for all classes, evenly
'''