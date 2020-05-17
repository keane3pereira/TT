from django.db import models
from timetable.data import classes_map
from django.utils import timezone

# Create your models here.

class Department(models.Model):
    name = models.CharField(max_length = 50, unique = True)
    LABS = models.IntegerField()
    CLASSROOMS = models.IntegerField()

    def __str__(self):
        return self.name

class Class(models.Model):
    department = models.ForeignKey(Department, on_delete = models.CASCADE)
    name = models.CharField(max_length = 50, unique = True)
    start_time = models.IntegerField()
    
    def __str__(self):
        return self.name

class Subject(models.Model):
    name = models.CharField(max_length = 50)
    CLASS = models.ForeignKey(Class, on_delete = models.CASCADE)
    TYPE = models.CharField(max_length = 50, default = "normal")
    teacher = models.CharField(max_length = 50)
    count = models.IntegerField()
    value = models.IntegerField()
    
    def __str__(self):
        return self.name

class Timetable(models.Model):
    department = models.ForeignKey(Department, on_delete=models.CASCADE)
    date_created = models.DateTimeField(default = timezone.now)
    
    def __str__(self):
        return self.dept + self.id

class Lecture(models.Model):
    timetable = models.ForeignKey(Timetable, on_delete=models.CASCADE)
    day = models.CharField(max_length = 50)
    time = models.CharField(max_length = 50)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE ,null = True)
    
    def __str__(self):
        return self.day + self.time