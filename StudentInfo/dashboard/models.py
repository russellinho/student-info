from django.db import models

class Student(models.Model):
    id = models.IntegerField(primary_key=True)
    first_name = models.CharField(max_length=20)
    last_name = models.CharField(max_length=20)
    enroll_date = models.DateTimeField('date published')

class Course(models.Model):
    id = models.IntegerField(primary_key=True)
    number = models.IntegerField()
    prefix = models.CharField(max_length=3)
    max_students = models.IntegerField(default=20)

class Enrollee(models.Model):
    studentId = models.ForeignKey(Student, on_delete=models.CASCADE)
    courseId = models.ForeignKey(Course, on_delete=models.CASCADE)
