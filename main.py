from flask import Flask, render_template, redirect
from data import teachers, teacher_count, classes_map, classes
from tt import Department, Class, Subject, TT, assign_teacher


app = Flask('my_app')

@app.route('/')
def main():
    from savefile import saved_tt
    data = {'tt': saved_tt}
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

    TTS = [TT(D) for _ in range(10)]
    min(TTS, key = lambda x : x.fitness).save_to_file()
    
    #T.display_grid()

    return redirect('/')


if __name__ == '__main__':
    app.run(debug = True, port = 5000)



'''
70 total, 35 * 3 + 35 * 2 = 175 total lectures per week / 6 = 29 per class avg / 6 days = 5 lectures per day avg.
1. Assign prac lectures for all classes, evenly
'''