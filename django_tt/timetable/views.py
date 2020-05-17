from django.shortcuts import render, redirect
from timetable.data import teachers, teacher_count, classes_map, classes, dept_details
from .models import Department, Class, Subject
import pickle

def assign_teacher():
    '''assigns subjects to teachers evenly'''
    global teacher_count
    teacher_count = (teacher_count + 1) % len(teachers)
    return teachers[teacher_count]

#views

def display_subjects(request):
    D = Department.objects.get(name = 'IT/CS')
    classes = Class.objects.filter(department = D)
    CLASSES = []
    subjects = Subject.objects.all()
    for c in classes:
        sub = subjects.filter(CLASS = c)
        DETAILS = {
            'name': c.name,
            'subjects': sub,
        }
        CLASSES.append(DETAILS)
    return render(request, 'subjects.html', {'CLASSES': CLASSES})

def main(request):
    try:
        file = open('savefile.p', 'rb')
        saved_tt = pickle.load(file)
        data = {'tt': saved_tt}
    except:
        data = None
    return render(request, 'main.html', {'data': data})
    
def create_subjects(request):
    Department.objects.all().delete()
    Subject.objects.all().delete()
    Class.objects.all().delete()
    print('deleted')

    ''' Input data '''
    D = Department(
            name = dept_details['name'],
            LABS = dept_details['labs'],
            CLASSROOMS = dept_details['classrooms']
        )
    D.save()

    for CLASS in classes_map:
        class_id = classes_map.index(CLASS)
        if class_id % 2 != 0: start_time = 2
        else: start_time = 0
        C = Class(
            department = D,
            name = CLASS,
            start_time = start_time
        )
        C.save()
        for subject in classes[CLASS]:
            teacher = assign_teacher()
            S = Subject(
                name = subject,
                CLASS = C,
                TYPE = 'normal',
                teacher = teacher,
                count = 3,
                value = 1
            )
            S.save()
            if S.name != 'SE': #se no prac
                P = Subject(
                    name = subject + ' P',
                    CLASS = C,
                    TYPE = 'prac',
                    teacher = teacher,
                    count = 1,
                    value = 2
                )
                P.save()
        print('class done')
    
    return redirect(display_subjects)


    ''' setting extra lectures '''
    '''D.CLASSES[2].SUBJECTS[0].running_behind += 2 #SE
    D.CLASSES[3].SUBJECTS[0].running_behind += 4 #CN
    D.CLASSES[3].SUBJECTS[1].running_behind -= 3 #LA'''
    '''
    T = TT(D)
    T.save_to_file()'''
    #x.display_grid()
    
    return redirect(main)